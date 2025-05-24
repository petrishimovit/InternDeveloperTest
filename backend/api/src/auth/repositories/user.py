from sqlalchemy.orm import Session
from auth.models.user import User
from auth.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate) -> User:

        hashed_password = pwd_context.hash(user.password)

        db_user = User(email=user.email, password=hashed_password)

        self.db.add(db_user)

        self.db.commit()

        self.db.refresh(db_user)
        return db_user