import json
from psycopg2 import connect
from fastapi import FastAPI
import pydantic
import uuid
import psycopg2

from pydantic import BaseModel

class user_request(BaseModel):
    name: str
    phone: str
    source: str
    comment: str

class LeadID(BaseModel):
    lead_id: str

api = FastAPI()

def get_conn():
    conn = psycopg2.connect(host="localhost", dbname="leads", user="user")

    return conn


@api.post("/leads")
def save_leads(request: user_request):
    conn = get_conn()

    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO leads (name, phone, source, comment , status) VALUES (%s,%s,%s,%s,%s) RETURNING lead_id",(request.name,request.phone,request.source,request.comment))

        lead_id = cur.fetchone()[0]

        event = {"lead_id": lead_id, "name": request.name, "phone":request.phone ,"source": request.source, "comment": request.comment}

        cur.execute("INSERT INTO outbox (event_type, aggregate_id, payload) VALUES(%s, %s, %s)",("leads_events.v1", lead_id, json.dumps(event)))

        conn.commit()
    except:
        conn.rollback()
        raise

    return {"lead_id":lead_id, "payload": json.dumps(event)}

@api.get("/leads/{lead_id}")
def get_lead_by_id(lead_id : str ):
    conn = get_conn()
    cur = conn.cursor()

    id = uuid.UUID(lead_id)

    try:
        cur.execute("SELECT * FROM leads WHERE lead_id = %s",(id,))
        responce = cur.fetchone()
    except:
        conn.rollback()

    if responce is None:
        return { "error": { "code": "lead_not_found", "message": "Заявка не найдена", "correlation_id":  str(uuid.uuid4())}}


    lead = {"name": responce[1], "phone": responce[2],"source": responce[3],"comment" : responce[4]}

    return {"lead_id":lead_id,"payload": json.dumps(lead)}
