import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.database import Base, get_db
from app.models.models import Customer, Product, wishlist_items
from app.core.auth import get_password_hash, create_access_token
from app.schemas.customer import CustomerCreate

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables before running tests
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # Create all tables for this test
    Base.metadata.create_all(bind=engine)

    # Create a new session for the test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_customer(db_session):
    customer_data = CustomerCreate(
        name="Test Customer", email="test@example.com", password="testpassword123"
    )
    customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        hashed_password=get_password_hash(customer_data.password),
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def test_product(db_session):
    product = Product(title="Test Product", price=99.99, brand="Test Brand")
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def token(test_customer):
    return create_access_token({"sub": test_customer.email})
