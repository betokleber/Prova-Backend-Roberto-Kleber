from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("", response_model=List[ProdutoResponse], status_code=status.HTTP_200_OK)
def listar_todos(db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.listar_produtos()

@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar(produto: ProdutoCreate, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.criar_produto(produto)

@router.get("/{id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def buscar_por_id(id: int, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.buscar_produto(id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remover(id: int, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    service.deletar_produto(id)
    return None