from fastapi import FastAPI

app = FastAPI(
    title="Luizalabs Wishlist API",
    description="API to manage a wishlist",
    version="0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
def read_root():
    return {"message": "LuiZalabs Wishlist API"}
