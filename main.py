from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Define a simple request model
class CarType(BaseModel):
    name: str
    type: str = Field(..., description="Type of the car, e.g., sedan, suv, etc.")
    price: float
    description: str = Field(..., description="A brief description of the car type")

class ResponseModel(BaseModel):
    price: float


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Car Price Estimator API"}

# Create a new item
@app.post("/carPriceEstimator")
def estimate_price(car: CarType) -> float:
    #pass cartype details to a mock prediction function
    base_price = car.price
    if car.type.lower() == "sedan":
        return base_price + 5000
    elif car.type.lower() == "suv":
        return base_price + 10000
    else:
        return base_price
