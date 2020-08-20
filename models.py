from sqlalchemy import Column, Integer, String, Float
from app import db


class DidNumber(db.Model):
    __tablename__ = 'did'
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)
    monthyPrice = Column(Float)
    setupPrice = Column(Float)
    currency = Column(String)
    

'''
{
  "id": 42,
  "valor": "+55 84 91234-4321",
  "monthyPrice": "0,03",
  "setupPrice": "3,40",
  "moeda": "U$"
}
'''
