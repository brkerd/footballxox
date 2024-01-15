from fastapi import FastAPI
from guessingEndpoints import router as guess_router

app = FastAPI()
app.include_router(guess_router,prefix="/api/v1")
