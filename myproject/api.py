from fastapi import FastAPI
from pydantic import BaseModel
from django.core.management import call_command
from myapp.models import Item
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

app = FastAPI()

class ItemModel(BaseModel):
    name: str
    description: str

@app.post("/items/")
def create_item(item: ItemModel):
    new_item = Item(name=item.name, description=item.description)
    new_item.save()
    return new_item

@app.get("/items/")
def read_items():
    return list(Item.objects.all().values())

@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemModel):
    existing_item = Item.objects.get(id=item_id)
    existing_item.name = item.name
    existing_item.description = item.description
    existing_item.save()
    return existing_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = Item.objects.get(id=item_id)
    item.delete()
    return {"message": "Item deleted"}
