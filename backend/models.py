from pydantic import BaseModel

class MealInput(BaseModel):
    meals: str
    goal: str


class UserRegister(BaseModel):
    username: str
    password: str
    age: int
    weight: float
    height: float

class UserLogin(BaseModel):
    username: str
    password: str

class DashboardRequest(BaseModel):
    username: str