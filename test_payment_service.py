#E2E

import requests
import random
import requests_mock
import enum
from datetime import datetime, timedelta


import pytest
import requests


class PaymentMethod(enum.Enum):
    NON_CASH = 'non_cash'
    CASH = 'cash'


class PaymentStatuses(enum.Enum):
    NOT_PAID = 'not_paid'
    PAID = 'paid'


class PaymentsAPI:
    # Инициализация с базовым URL API
    def __init__(self, base_url: str):
        self.base_url = base_url

    # Метод получения всех возвратов
    def get_all_payments(self):
        url = f"{self.base_url}get_all_payments"
        # Отправка GET-запроса и возврат ответа в формате JSON
        response = requests.get(url).json()
        return response

    # Метод получения возврата по ID
    def get_payments_by_id(self, payments_id: int):
        url = f"{self.base_url}{payments_id}"
        response = requests.get(url).json()
        return response


# Фикстура для тестирования, создающая экземпляр API
@pytest.fixture()
def api():
    # Создание экземпляра PaymentsAPI с базовым URL
    return PaymentsAPI('http://localhost:8010/api/payments/')


def test_get_all_payments(api):
    response = api.get_all_payments()
    assert (response == [
        {'id': 1, 'purchase_id': 1, 'date': '2020-01-01 04:42:05.427694', 'method': 'non_cash', 'status': 'paid'},
        {'id': 2, 'purchase_id': 2, 'date': '2020-01-02 04:42:05.427694', 'method': 'cash', 'status': 'non_paid'},
        {'id': 3, 'purchase_id': 3, 'date': '2020-01-03 04:42:05.427694', 'method': 'cash', 'status': 'paid'}
    ])


def test_get_payments_by_id(api):
    response = api.get_payments_by_id(1)
    assert (response ==
           {'id': 1, 'purchase_id': 1, 'date': '2020-01-01 04:42:05.427694', 'method': 'non_cash', 'status': 'paid'})


def test_get_payments_by_id_invalid(api: PaymentsAPI):
    # Проверка на получение информации о несуществующей компании
    response = api.get_payments_by_id(99)
    assert (response == None)


if __name__ == '__main__':
    URL = 'http://localhost:80/api/payments/'
    api = PaymentsAPI(URL)
    test_get_all_payments(api)
    test_get_payments_by_id(api)



#base_url = 'http://payment-service:8010/api/payments/'
#
#purchase_id = random.randint(1, 100)
#key_id = random.randint(1, 100)
#date = datetime.now() - timedelta(days=random.randrange(3650), seconds=random.randrange(86400))
#status = random.choice(list(PaymentStatuses))
#method = random.choice(list(PaymentMethod))
#
#mock_payment_data = [
#    {'id': 1, 'purchase_id': purchase_id, 'date': str(date), 'method': str(method), 'status': str(status)},
#    {'id': 2, 'purchase_id': purchase_id, 'date': str(date), 'method': str(method), 'status': str(status)},
#    {'id': 3, 'purchase_id': purchase_id, 'date': str(date), 'method': str(method), 'status': str(status)}
#]
#
#
#def mock_request(adapter):
#    adapter.register_uri('GET', f'{base_url}get_payments', json={'detail': 'Not Found'}, status_code=404)
#
#
## Тест получения пустых payments
#def test_get_payment_empty() -> None:
#    with requests_mock.Mocker() as m:
#        mock_request(m)
#        response = requests.get(f'{base_url}get_payments')
#        assert response.json() == {'detail': 'Not Found'}
#        assert response.status_code == 404
#
#
#def mock_request_with_data(adapter):
#    adapter.register_uri('GET', f'{base_url}get_payments', json=mock_payment_data, status_code=200)
#
#
## Тест получения всех payments
#def test_get_payment_filled() -> None:
#    with requests_mock.Mocker() as m:
#        mock_request_with_data(m)
#        response = requests.get(f'{base_url}get_payments')
#        assert response.json() == mock_payment_data
#        assert response.status_code == 200
#
#
#def mock_request_with_data_by_id(adapter, payment_id, payment_data):
#    # Регистрация маршрута для конкретного ID платежа
#    adapter.register_uri('GET', f'{base_url}{payment_id}/', json=payment_data, status_code=200)
#
#
## Тест получения payments по id
#def test_get_payment_by_id_found():
#    with requests_mock.Mocker() as m:
#        # Регистрации маршрута с помощью адаптера
#        mock_request_with_data_by_id(m, mock_payment_data[0]['id'], mock_payment_data[0])
#        response = requests.get(f'{base_url}{mock_payment_data[0]["id"]}/')
#        assert response.status_code == 200
#        assert response.json() == mock_payment_data[0]
#
#
## Тест получения несуществующего payments
#def test_get_payment_by_id_not_found():
#    with requests_mock.Mocker() as m:
#        m.register_uri('GET', f'{base_url}123/', json={'detail': 'Payments not found'}, status_code=404)
#        response = requests.get(f'{base_url}123/')
#        assert response.status_code == 404
#        assert response.json() == {'detail': 'Payments not found'}
#
#
## Тест удаления payments по id {base_url}{id}
#def test_delete_payment():
#    with requests_mock.Mocker() as m:
#        id_key = 1
#        # Регистрации маршрута с помощью адаптера
#        mock_request_with_data_by_id(m, id_key, mock_payment_data)
#        # Регистрация маршрута для DELETE запроса
#        m.delete(f'{base_url}1/', json={'message': f'Payment with ID {id_key} has been successfully deleted'},
#                 status_code=200)
#        m.delete(f'{base_url}99/', json={'detail': 'Payment not found'}, status_code=404)
#        response = requests.delete(f'{base_url}{id_key}/')
#        # Проверка успешного удаления payments
#        assert response.status_code == 200
#        assert response.json() == {'message': f'Payment with ID {id_key} has been successfully deleted'}
#        # Проверка попытки удаления несуществующего payments
#        response = requests.delete(f'{base_url}99/')
#        assert response.status_code == 404
#        assert response.json() == {'detail': 'Payment not found'}


