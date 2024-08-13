from fastapi import FastAPI
from model import cal_size
from pydantic import BaseModel

app = FastAPI();

class ImageUrl(BaseModel):
    image_url: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict(data: ImageUrl):
    measurements = cal_size(data.image_url)
    return measurements