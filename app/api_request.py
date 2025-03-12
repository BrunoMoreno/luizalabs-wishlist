import requests
import json


def get_data():
    response = requests.get("https://luizalabs-api.onrender.com/products")
    return response.json()


def get_product_by_id(product_id):
    response = requests.get(f"https://luizalabs-api.onrender.com/products/{product_id}")
    return response.json()
