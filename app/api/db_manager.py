from fastapi import HTTPException
from models import PaymentIn
from db import payments, database


async def add_payment(payload: PaymentIn):
    try:
        query = payments.insert().values(**payload.dict())
        return await database.execute(query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_all_payments():
    try:
        query = payments.select()
        result = await database.fetch_all(query=query)
        if result:
            return result
        raise HTTPException(status_code=404, detail='Payments not found')
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_payment(id):
    try:
        query = payments.select().where(payments.c.id == id)
        result = await database.fetch_one(query=query)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


async def get_purchase_id(purchase_id: int):
    try:
        query = payments.select().where(payments.c.purchase_id == purchase_id)
        return await database.fetch_one(query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


async def delete_payment(id: int):
    try:
        query = payments.delete().where(payments.c.id == id)
        result = await database.execute(query=query)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')
