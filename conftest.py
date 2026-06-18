import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_TEST = "postgresql://postgres:postgres_pwd@localhost:5433/ecom_test"
os.environ["DATABASE_URL"] = DATABASE_URL_TEST
os.environ["ENV"] = "testing"

from app.main import app
from app.core.config import Base
from app.core.dependencies import get_db

engine_test = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine_test)
    
    def _get_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = _get_db_override
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def produto_existente(client):
    payload = {"nome": "Produto Base", "preco": 99.90, "estoque": 2}
    response = client.post("/produtos", json=payload)
    return response.json()