import requests
from fastapi import HTTPException
from requests import RequestException

#PURCHASE_SERVICE_HOST_URL = 'http://127.0.0.1:8020/api/purchases/get_purchases'
#PURCHASE_SERVICE_HOST_URL = 'http://purchase_service:8020/api/purchases/get_purchases'
#
#
#def is_purchase_present(purchase_id: int):
#    try:
#        response = requests.get(PURCHASE_SERVICE_HOST_URL)
#        response.raise_for_status()
#        data = response.json()
#        id_list = [item['id'] for item in data]
#        return purchase_id in id_list
#    except RequestException as e:
#        raise HTTPException(status_code=500, detail='Service unavailable')
