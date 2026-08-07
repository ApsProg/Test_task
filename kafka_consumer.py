import json
import time

from aiokafka import AIOKafkaConsumer

from post import get_conn

consumer = AIOKafkaConsumer("lead_moderation.events.v1", bootstrap_servers= 'localhost:7777', group_id='lead_moderation_consumer', auto_offset_reset='earliest')

def find_inbound_event_by_id(event_id, conn):

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM inbound_events WHERE event_id = %s ",(event_id,))

        if cur.fetchone() == None:
            return False
        else:
            return True
    except Exception as e:
        raise e
    finally:
        cur.close()


def handle_event(event, conn):

    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO inbound_events (event_id) VALUES (%s)",(event["event_id"],))
        status = "rejected"
        if event["payload"]["approved"]:
            status = "approved"
        cur.execute("UPDATE leads SET status = %s WHERE lead_id = %s",(status,event["aggregate_id"]))
        conn.commit()
    except Exception as e:
        raise e

async def kafka_consumer():

    conn = get_conn()

    await consumer.start()

    try:
        async for msg in consumer:
            event = json.loads(msg.value)

            try:
                if find_inbound_event_by_id(event["event_id"], conn):
                    continue
                handle_event(event, conn)
            except:
                time.sleep(5)

    finally:
        await consumer.stop()
