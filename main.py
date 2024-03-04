from fastapi import FastAPI
from guessingEndpoints import router as guess_router
from player import playerRouter
app = FastAPI()
app.include_router(guess_router,prefix="/api/v1")
app.include_router(playerRouter)
