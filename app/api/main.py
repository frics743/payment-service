import random
from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter
from payments import payments
from db import metadata, database, engine
from models import PaymentMethod, PaymentStatuses

app = FastAPI(title='Online store of board games: Payment', openapi_url="/api/payments/openapi.json",
              docs_url="/api/payments/docs")

date = datetime.now() - timedelta(days=random.randrange(3650), seconds=random.randrange(86400))
status = random.choice(list(PaymentStatuses))
method = random.choice(list(PaymentMethod))
payments_router = APIRouter()

payment_data = [
    {'id': 1, 'purchase_id': '1', 'date': str(date), 'method': str(method), 'status': str(status)},
    {'id': 2, 'purchase_id': '2', 'date': str(date), 'method': str(method), 'status': str(status)},
    {'id': 3, 'purchase_id': '3', 'date': str(date), 'method': str(method), 'status': str(status)}
]


#/api/payments/get_all_payments
@payments_router.get("/get_all_payments")
async def read_payments():
    return payment_data


#/api/payments/{payments_id}?payment_id=1
@payments_router.get("/{payments_id}")
async def read_payment(payment_id: int):
    for payment in payment_data:
        if payment['id'] == payment_id:
            return payment
    return None

app.include_router(payments_router, prefix='/api/payments', tags=['payments'])
