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



app.include_router(payments, prefix='/api/payments', tags=['Payments'])


if __name__ == '__main__':
    import uvicorn
    import os
    try:
        PORT = int(os.environ['PORT'])
    except KeyError as keyerr:
        PORT = 80
    uvicorn.run(app, host='0.0.0.0', port=PORT)
