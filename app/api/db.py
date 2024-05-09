from sqlalchemy import (Column, DateTime, Integer, MetaData, Table, create_engine, ARRAY, Enum, func)
from databases import Database
from models import PaymentMethod, PaymentStatuses

#DATABASE_URI = 'postgresql://admin:adminadmin@127.0.0.1:5432/postgres'
DATABASE_URI = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

payments = Table(
    'payment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('purchase_id', Integer),
    Column('date', DateTime, default=func.now()),
    Column('amount', Integer),
    Column('method', Enum(PaymentMethod)),
    Column('status', Enum(PaymentStatuses))
)

database = Database(DATABASE_URI)
