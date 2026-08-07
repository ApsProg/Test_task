import json
import time

from fileinput import close

import psycopg2

from post import get_conn

from aiokafka import AIOKafkaProducer

producer = AIOKafkaProducer(bootstrap_servers='localhost:7777')


def get_unpublished_messages(conn):
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT * FROM outbox WHERE status = %s """,("NEW",))

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No new outbox messages")
            conn.rollback()
            return []

        unpublished_messages = []
        for row in rows:
            unpublished_messages.append({"event_id":row[0], "event_type": row[1], "aggregate_id": row[2], "occured_at": row[3], "payload": row[4]})

        return unpublished_messages


    except Exception as e:
        conn.rollback()
        raise e
def mark_published(event_id, conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
        UPDATE outbox SET status = %s WHERE event_id = %s  """,("PUBLISHED",event_id))
        conn.commit()
    except:
        conn.rollback()
async def outbox_publisher():

    conn = get_conn()

    while True:
        try:
            unpublished_messages = get_unpublished_messages(conn)

            ids = []

            for message in unpublished_messages:
                ids.append(message["event_id"])
                await producer.send_and_wait('leads.events.v1', json.dumps(message).encode('utf-8'))
                mark_published(message["event_id"], conn)
                await producer.stop()
                time.sleep(10)
        except Exception as e:
            time.sleep(5)
        time.sleep(5)

