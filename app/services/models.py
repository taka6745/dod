from sqlalchemy import Column, Integer, String, Time, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

class Roster(Base):
    __tablename__ = 'rosters'

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    business_hours = Column(DECIMAL(5, 2))
    after_hours = Column(DECIMAL(5, 2))
