from fastapi import FastAPI
from app.api.v1 import routes_auth


app = FastAPI(title="Estimation AI Backend")

@app.get("/")
def rootz():
    return {"message": "Estimation AI Backend running"}

app.include_router(routes_auth.router,prefix="/api/v1/auth",tags=["auth"])