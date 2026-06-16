from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

import models, schemas, auth, database
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitNova AI - Premium Fitness API")

# Authentication
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# BMI History
@app.post("/save-bmi", response_model=schemas.BMIRecord)
def save_bmi(record: schemas.BMICreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_record = models.BMIRecord(**record.dict(), owner_id=current_user.id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/bmi-history", response_model=List[schemas.BMIRecord])
def get_bmi_history(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.BMIRecord).filter(models.BMIRecord.owner_id == current_user.id).all()

# Calories History
@app.post("/save-calories", response_model=schemas.CalorieRecord)
def save_calories(record: schemas.CalorieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_record = models.CalorieRecord(**record.dict(), owner_id=current_user.id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/calories-history", response_model=List[schemas.CalorieRecord])
def get_calories_history(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.CalorieRecord).filter(models.CalorieRecord.owner_id == current_user.id).all()

# Water History
@app.post("/save-water", response_model=schemas.WaterRecord)
def save_water(record: schemas.WaterCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_record = models.WaterRecord(**record.dict(), owner_id=current_user.id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/water-history", response_model=List[schemas.WaterRecord])
def get_water_history(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.WaterRecord).filter(models.WaterRecord.owner_id == current_user.id).all()

# Goals
@app.post("/save-goals", response_model=schemas.Goal)
def save_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_goal = models.Goal(**goal.dict(), owner_id=current_user.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.get("/goals", response_model=List[schemas.Goal])
def get_goals(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Goal).filter(models.Goal.owner_id == current_user.id).all()

# Workouts
@app.post("/save-workouts", response_model=schemas.Workout)
def save_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_workout = models.Workout(**workout.dict(), owner_id=current_user.id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.get("/workouts", response_model=List[schemas.Workout])
def get_workouts(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Workout).filter(models.Workout.owner_id == current_user.id).all()

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
