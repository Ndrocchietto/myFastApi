from typing import Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

## This app is the same one referred by uvicorn in the command:uvicorn main:app --reload
# The command uvicorn main:app refers to:

#     main: the file main.py (the Python "module").
#     app: the object created inside of main.py with the line app = FastAPI().
#     --reload: make the server restart after code changes. Only do this for development.
app = FastAPI() 

class Item(BaseModel):
    name:str ="ciaociao "
    price:float
    is_offer: Union[bool, None] = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:

#     the path /
#     using a get operation
# That @something syntax in Python is called a "decorator".

# You put it on top of a function. Like a pretty decorative hat 
# It is the "PATH OPERATION decorator"
@app.get("/")
def read_root():
    return {"Hello": "World"}

#path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
#Otherwise, the path  that comes in the method after this one for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me"
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

# The value of the PATH PARAMETER item_id will be passed to your function as the argument item_id.
# So, if you run this example and go to http://127.0.0.1:8000/items/foo, you will see a response of:
# {"item_id":"foo"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

## try the put via swagger http://127.0.0.1:8000/docs or redoc http://127.0.0.1:8000/redoc
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}

# In this case, the function parameter q will be optional, and will be None by default.
@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/items3/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": # this is another construction to show one can use `value`#test

        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
