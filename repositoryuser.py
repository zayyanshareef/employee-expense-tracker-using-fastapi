from sqlalchemy.orm import Session
from models import UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserModel):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str):
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()
