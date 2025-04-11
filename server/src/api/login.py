from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from server.src.db.session import get_db
from server.src.db import crud
from server.src.rabbitmq.notification import remove_user_notifications
from server.src.caching.cleanup import clear_user_cache
from server.src.utils.security import verify_password, create_access_token, decode_access_token
from server.src.api.schemas import UserCreate, UserUpdate, UserResponse, Token
from server.src.rabbitmq.rmq import publish_message
from server.src.rabbitmq.schemas import NotificationMessage


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = crud.create_user(db=db, username=user.username, email=user.email, password=user.password)

    # Publish a RabbitMQ notification
    message = NotificationMessage(user_id=new_user.id, message="New user registered")
    publish_message('user.signup', message)

    return new_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_user_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@app.put("/users/me", response_model=UserResponse)
def update_user_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return crud.update_user(db=db, user_id=current_user.id, **user_update.dict(exclude_unset=True))

@app.delete("/users/me", response_model=UserResponse)
def delete_user_me(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    # Remove user-related data from RabbitMQ
    remove_user_notifications(db, current_user.id)
    
    # Clear user-related cache from Redis
    clear_user_cache(current_user.id)
    
    # Delete the user and all related data
    crud.delete_user(db=db, user_id=current_user.id)
    return current_user

@app.put("/users/me/password", response_model=UserResponse)
def update_password(current_password: str, new_password: str, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    return crud.update_user_password(db=db, user_id=current_user.id, password=new_password)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
