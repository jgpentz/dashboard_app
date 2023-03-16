from typing import Union
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from rf_gain import GainProcessor
from failure_types import FailureTypes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
gainprocessor = GainProcessor()
failuretypes = FailureTypes()

origins = [
    "http://localhost:3001",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/rf_gain")
async def read_rf_gains():
    return {"data" : gainprocessor.get_dataframes()}

@app.get("/failure_types")
async def read_failure_types():
    return {"data" : failuretypes.get_data()}

if __name__ == "__main__":
    uvicorn.run(app, port=int("8001"))