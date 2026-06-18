from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.produto import ProdutoModel
from app.schemas.produto import ProdutoCreate

class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ProdutoModel]:
        return self.db.query(ProdutoModel).all()

    def get_by_id(self, produto_id: int) -> Optional[ProdutoModel]:
        return self.db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()

    def create(self, produto: ProdutoCreate) -> ProdutoModel:
        db_produto = ProdutoModel(**produto.model_dump())
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto

    def delete(self, db_produto: ProdutoModel) -> None:
        self.db.delete(db_produto)
        self.db.commit()