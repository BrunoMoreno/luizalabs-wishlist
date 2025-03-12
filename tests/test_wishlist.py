import pytest
from fastapi import status


def test_get_empty_wishlist(client, token):
    response = client.get("/wishlist", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["products"]) == 0


def test_add_product_to_wishlist(client, token, test_product):
    product_id = str(test_product.id)
    response = client.post(
        f"/wishlist/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Verify product is in wishlist
    response = client.get("/wishlist", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["products"]) == 1
    assert data["products"][0]["id"] == product_id


def test_add_nonexistent_product(client, token):
    response = client.post(
        "/wishlist/products/nonexistent", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found"


def test_add_duplicate_product(client, token, test_product):
    product_id = str(test_product.id)
    # Add product first time
    response = client.post(
        f"/wishlist/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Try to add same product again
    response = client.post(
        f"/wishlist/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Product already in wishlist"


def test_remove_product_from_wishlist(client, token, test_product):
    product_id = str(test_product.id)
    # Add product first
    client.post(
        f"/wishlist/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Remove product
    response = client.delete(
        f"/wishlist/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify product is removed
    response = client.get("/wishlist", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["products"]) == 0


def test_remove_nonexistent_product(client, token):
    response = client.delete(
        "/wishlist/products/nonexistent", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found"


def test_wishlist_product_details(client, token, test_product):
    product_id = str(test_product.id)
    product_title = test_product.title
    product_price = test_product.price
    product_image = test_product.image
    product_brand = test_product.brand
    product_review_score = test_product.review_score

    # Add product to wishlist
    client.post(
        f"/wishlist/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Get wishlist and verify product details
    response = client.get("/wishlist", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    product = data["products"][0]
    assert product["id"] == product_id
    assert product["title"] == product_title
    assert product["price"] == product_price
    assert product["image"] == product_image
    assert product["brand"] == product_brand
    assert product["review_score"] == product_review_score
