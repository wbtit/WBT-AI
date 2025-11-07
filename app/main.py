from fastapi import FastAPI
from app.api.v1 import routes_auth
from app.api.v1.estimation import estimation_router
from app.api.v1.project import project_router
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Estimation AI Backend")

@app.get("/")
def rootz():
    return {"message": "Estimation AI Backend running"}

app.include_router(routes_auth.router,prefix="/api/v1/auth",tags=["auth"])

app.include_router(estimation_router.router,prefix="/api/v1/estimation",tags=["estimation"])
app.include_router(project_router.router,prefix="/api/v1/project",tags=["project"])