from fastapi import FastAPI


app = FastAPI(title="Estimation AI Backend")

@app.get("/")
def rootz():
    return {"message": "Estimation AI Backend running"}