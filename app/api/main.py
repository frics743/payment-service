import random
from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter
from payments import payments
from db import metadata, database, engine
from models import PaymentMethod, PaymentStatuses

app = FastAPI(title='Online store of board games: Payment', openapi_url="/api/payments/openapi.json",
              docs_url="/docs")

date = datetime.now() - timedelta(days=random.randrange(3650), seconds=random.randrange(86400))
status = random.choice(list(PaymentStatuses))
method = random.choice(list(PaymentMethod))
payments_router = APIRouter()

payment_data = [
    {'id': 1, 'purchase_id': 1, 'date': '2020-01-01 04:42:05.427694', 'method': 'non_cash', 'status': 'paid'},
    {'id': 2, 'purchase_id': 2, 'date': '2020-01-02 04:42:05.427694', 'method': 'cash', 'status': 'non_paid'},
    {'id': 3, 'purchase_id': 3, 'date': '2020-01-03 04:42:05.427694', 'method': 'cash', 'status': 'paid'}
]


#/api/payments/get_all_payments
@payments_router.get("/get_all_payments")
async def get_all_payments():
    return payment_data


#/api/payments/{payments_id}?payment_id=1
@payments_router.get("/{payments_id}")
async def get_payments_id(payments_id: int):
    for payment in payment_data:
        if payment['id'] == payments_id:
            return payment
    return None

app.include_router(payments_router, prefix='/api/payments', tags=['payments'])

#ssfdg