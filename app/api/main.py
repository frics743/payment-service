from fastapi import FastAPI
from payments import payments
from db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(title='Online store of board games: Payment')


@app.on_event('startup')
async def startup_event():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()




#@app.get('/', tags=['Запуск'])
#async def startup():
#    await database.connect()
#    return 'База данных присоеденена'

#payments_router = APIRouter()

#paymentss = [
#    {'artists_id': 1,
#     'name': 'Kany West',
#     'age': '47',
#     'auditions': '1 billion',
#     'genre': 'rap, R&B, electronic, gospel'},
#    {'artists_id': 2,
#     'name': 'Валерий Меладзе',
#     'age': '58',
#     'auditions': '45 millions',
#     'genre': 'поп, рок, эстрадная песня'},
#    {'artists_id': 3,
#     'name': 'Billie Eilish',
#     'age': '22',
#     'auditions': '300 millions',
#     'genre': 'rap, pop'},
#    {'artists_id': 4,
#     'name': 'The Weeknd',
#     'age': '34',
#     'auditions': '700 millions',
#     'genre': 'rap, R&B'},
#    {'artists_id': 5,
#     'name': 'Eminem',
#     'age': '51',
#     'auditions': '1 billion',
#     'genre': 'rap, hip-hop'}
#]


#@payments_router.get("/")
#async def read_payments():
#    return payments
#
#
#@payments_router.get("/{payments_id}")
#async def read_paymentt(payments_id: int):
#    for payment in payments:
#        if payment['payments_id'] == payments_id:
#            return payment
#    return None

app.include_router(payments, prefix='/api/payments', tags=['Payments'])


#if __name__ == '__main__':
#    import uvicorn
#    import os
#    try:
#        PORT = int(os.environ['PORT'])
#    except KeyError as keyerr:
#        PORT = 80
#    uvicorn.run(app, host='0.0.0.0', port=PORT)
