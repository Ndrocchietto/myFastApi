from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() ## This app is the same one referred by uvicorn in the command:uvicorn main:app --reload

class Item(BaseModel):
    name:str ="ciaociao "
    price:float
    is_offer: Union[bool, None] = None


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