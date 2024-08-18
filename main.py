from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from projects.router import router as project_router
from users.router import router as user_router
from fastapi.middleware.cors import CORSMiddleware

import uvicorn


app = FastAPI(title="ІТ-ПАРОСТОК")

# connect work with static files (images)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(project_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)  # або в терміналі uvicorn main:app --reload
