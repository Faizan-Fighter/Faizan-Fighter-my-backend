from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    bmi_records = relationship("BMIRecord", back_populates="owner")
    calorie_records = relationship("CalorieRecord", back_populates="owner")
    water_records = relationship("WaterRecord", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")
    workouts = relationship("Workout", back_populates="owner")

class BMIRecord(Base):
    __tablename__ = "bmi_records"
    id = Column(Integer, primary_key=True, index=True)
    bmi_value = Column(Float)
    weight = Column(Float)
    height = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bmi_records")

class CalorieRecord(Base):
    __tablename__ = "calorie_records"
    id = Column(Integer, primary_key=True, index=True)
    calories = Column(Integer)
    activity = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="calorie_records")

class WaterRecord(Base):
    __tablename__ = "water_records"
    id = Column(Integer, primary_key=True, index=True)
    amount_ml = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="water_records")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    target_value = Column(Float)
    current_value = Column(Float, default=0.0)
    deadline = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="goals")

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    workout_type = Column(String)
    duration_minutes = Column(Integer)
    intensity = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="workouts")
