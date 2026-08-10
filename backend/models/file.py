from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    filepath = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    owner = relationship(
    "User",
    back_populates="files"
    )
    