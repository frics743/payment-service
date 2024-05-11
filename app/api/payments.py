from typing_extensions import List, Annotated
from fastapi import APIRouter, HTTPException, Depends
from models import PaymentOut, PaymentIn
from db_manager import add_payment, get_payment, get_all_payments, delete_payment, get_purchase_id
from service import is_purchase_present

payments = APIRouter()


@payments.post('/create_payment', response_model=PaymentIn, status_code=201)
async def create_payment(payload: Annotated[PaymentIn, Depends()]):
    purchase_id = payload.purchase_id
    try:
        if is_purchase_present(purchase_id):
            existing_payment = await get_payment(purchase_id)
            existing_purchase = await get_purchase_id(purchase_id)
            if existing_payment or existing_purchase:
                raise HTTPException(status_code=400,
                                    detail=f'Payment for purchase with id:{purchase_id} already exists')
            payment_id = await add_payment(payload)
            response = {
                'id': payment_id,
                **payload.dict()
            }
            return response
        else:
            raise HTTPException(status_code=404, detail=f'Purchase with given id:{purchase_id} not found')
    except HTTPException as http_exc:
        # Переопределение исключений от функций add_payment(), get_payment(), get_purchase_id()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


@payments.get('/get_payments', response_model=List[PaymentOut])
async def get_payments():
    try:
        result = await get_all_payments()
        if result is None:
            raise HTTPException(status_code=404, detail='Payments not found')
        return result
    except HTTPException as http_exc:
        # Переадресация исключений от функции get_all_payments()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


@payments.get('/{id}/', response_model=PaymentOut)
async def get_payment_by_id(id: int):
    try:
        payments_by_id = await get_payment(id)
        if not payments_by_id:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payments_by_id
    except HTTPException as http_exc:
        # Переопределение исключений от функции get_payment()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')


@payments.delete('/{id}/', response_model=None)
async def delete_payment_from_db(id: int):
    try:
        payments_by_id = await get_payment(id)
        if not payments_by_id:
            raise HTTPException(status_code=404, detail='Payment not found')
        await delete_payment(id)
        return {'message': f'Payment with ID {id} has been successfully deleted'}
    except HTTPException as http_exc:
        # Переопределение исключений от функции get_payment()
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal server error')
