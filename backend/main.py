from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.api import auth, users, ai_model  

from fastapi.middleware.cors import CORSMiddleware

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Wealth Advisor")

origins = ["http://localhost:5173"]  # frontend dev server

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ai_model.router)  

@app.get("/")
def root():
    return {"message": "AI Wealth Advisor Backend Running"}