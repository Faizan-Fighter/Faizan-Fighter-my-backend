from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# BMI Schemas
class BMIBase(BaseModel):
    bmi_value: float
    weight: float
    height: float

class BMICreate(BMIBase):
    pass

class BMIRecord(BMIBase):
    id: int
    timestamp: datetime
    owner_id: int
    class Config:
        from_attributes = True

# Calorie Schemas
class CalorieBase(BaseModel):
    calories: int
    activity: str

class CalorieCreate(CalorieBase):
    pass

class CalorieRecord(CalorieBase):
    id: int
    timestamp: datetime
    owner_id: int
    class Config:
        from_attributes = True

# Water Schemas
class WaterBase(BaseModel):
    amount_ml: int

class WaterCreate(WaterBase):
    pass

class WaterRecord(WaterBase):
    id: int
    timestamp: datetime
    owner_id: int
    class Config:
        from_attributes = True

# Goal Schemas
class GoalBase(BaseModel):
    title: str
    target_value: float
    current_value: float = 0.0
    deadline: datetime

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

# Workout Schemas
class WorkoutBase(BaseModel):
    workout_type: str
    duration_minutes: int
    intensity: str

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    id: int
    timestamp: datetime
    owner_id: int
    class Config:
        from_attributes = True
