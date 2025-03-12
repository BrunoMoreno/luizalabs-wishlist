from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Annotated
from app.db.database import get_db, engine
from app.models import models
from app.schemas import schemas
from app.core.auth import (
    get_current_user,
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Luizalabs Wishlist API",
    description="API to manage a wishlist",
    version="0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.Customer)
        .filter(models.Customer.email == form_data.username)
        .first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/customers", response_model=schemas.Customer)
async def create_customer(
    customer: schemas.CustomerCreate, db: Session = Depends(get_db)
):
    db_customer = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email)
        .first()
    )
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(customer.password)
    db_customer = models.Customer(
        email=customer.email, name=customer.name, hashed_password=hashed_password
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.get("/customers/me", response_model=schemas.Customer)
async def read_users_me(
    current_user: Annotated[models.Customer, Depends(get_current_user)],
):
    return current_user


@app.put("/customers/me", response_model=schemas.Customer)
async def update_customer(
    customer_update: schemas.CustomerUpdate,
    current_user: models.Customer = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if customer_update.email and customer_update.email != current_user.email:
        if (
            db.query(models.Customer)
            .filter(models.Customer.email == customer_update.email)
            .first()
        ):
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = customer_update.email

    if customer_update.name:
        current_user.name = customer_update.name

    if customer_update.password:
        current_user.hashed_password = get_password_hash(customer_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@app.delete("/customers/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    current_user: models.Customer = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.delete(current_user)
    db.commit()


@app.get("/wishlist", response_model=schemas.WishlistResponse)
async def get_wishlist(current_user: models.Customer = Depends(get_current_user)):
    return {
        "products": [
            {**product.__dict__, "id": str(product.id)}
            for product in current_user.products
        ]
    }


@app.post("/wishlist/products/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_product_to_wishlist(
    product_id: str,
    current_user: models.Customer = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        product_id_int = int(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if product exists in the products table
    product = (
        db.query(models.Product).filter(models.Product.id == product_id_int).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if product is already in wishlist
    if product in current_user.products:
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    # Add product to wishlist
    current_user.products.append(product)
    db.commit()
    return {"message": "Product added to wishlist"}


@app.delete("/wishlist/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_wishlist(
    product_id: str,
    current_user: models.Customer = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        product_id_int = int(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if product exists in the products table
    product = (
        db.query(models.Product).filter(models.Product.id == product_id_int).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if product is in wishlist
    if product not in current_user.products:
        raise HTTPException(status_code=404, detail="Product not in wishlist")

    # Remove product from wishlist
    current_user.products.remove(product)
    db.commit()
