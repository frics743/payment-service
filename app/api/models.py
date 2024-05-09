import enum
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional


class PaymentMethod(enum.Enum):
    NON_CASH = 'non_cash'
    CASH = 'cash'


class PaymentStatuses(enum.Enum):
    NOT_PAID = 'not_paid'
    PAID = 'paid'


class PaymentIn(BaseModel):
    purchase_id: int
    date: Optional[datetime] = None
    method: PaymentMethod
    status: PaymentStatuses


class PaymentOut(PaymentIn):
    id: int
