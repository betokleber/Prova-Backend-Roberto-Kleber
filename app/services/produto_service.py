from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto import ProdutoCreate
from app.models.produto import ProdutoModel

class ProdutoService:
    def __init__(self, db: Session):
        self.repository = ProdutoRepository(db)

    def listar_produtos(self) -> List[ProdutoModel]:
        return self.repository.get_all()

    def buscar_produto(self, produto_id: int) -> ProdutoModel:
        produto = self.repository.get_by_id(produto_id)
        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return produto

    def criar_produto(self, produto: ProdutoCreate) -> ProdutoModel:
        return self.repository.create(produto)

    def deletar_produto(self, produto_id: int) -> None:
        produto = self.buscar_produto(produto_id)
        self.repository.delete(produto)