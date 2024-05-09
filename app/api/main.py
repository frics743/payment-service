import random
from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter
from payments import payments
from db import metadata, database, engine
from models import PaymentMethod, PaymentStatuses

#metadata.create_all(engine)

app = FastAPI(title='Online store of board games: Payment', openapi_url="/api/payments/openapi.json",
              docs_url="/api/payments/docs")

purchase_id = random.randint(1, 100)
key_id = random.randint(1, 100)
date = datetime.now() - timedelta(days=random.randrange(3650), seconds=random.randrange(86400))
status = random.choice(list(PaymentStatuses))
method = random.choice(list(PaymentMethod))
payments_router = APIRouter()

payment_data = [
    {'id': 1, 'purchase_id': purchase_id, 'date': str(date), 'method': str(method), 'status': str(status)},
    {'id': 2, 'purchase_id': purchase_id, 'date': str(date), 'method': str(method), 'status': str(status)},
    {'id': 3, 'purchase_id': purchase_id, 'date': str(date), 'method': str(method), 'status': str(status)}
]


@payments_router.get("/")
async def read_payment():
    return payment_data


@payments_router.get("/{payments_id}")
async def read_artist(payment_id: int):
    for payment in payment_data:
        if payment['payments_id'] == payment_id:
            return payment
    return None


@payments_router.get("/get_all_payments")
async def read_artist():
    return 'Hello World'


#@app.on_event('startup')
#async def startup_event():
#    await database.connect()
#
#
#@app.on_event('shutdown')
#async def shutdown():
#    await database.disconnect()

app.include_router(payments_router, prefix='/api/payments', tags=['payments'])

#app.include_router(payments, prefix='/api/payments', tags=['Payments'])

