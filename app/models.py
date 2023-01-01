from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(String(64), primary_key=True, default=str(uuid4()))
    username = Column(String(64), index=True, unique=True)
    email = Column(String(64), index=True, unique=True)
    password_hash = Column(String(128))
    posts = relationship("Post", backref="user")

    def __repr__(self) -> str:
        return f"<User id: {self.id}, username:{self.username}, email:{self.email}, password:{self.password_hash}>"


class Post(Base):
    __tablename__ = "post"
    id = Column(String(64), primary_key=True, default=str(uuid4()))
    title = Column(String(64), index=True, unique=True)
    content = Column(String(256), index=True, nullable=False)
    user_id = Column(String(64), ForeignKey("user.id"), nullable=False)
    timestamp = Column(DateTime, index=True, default=datetime.now())
    category_id = Column(
        String(64), ForeignKey("category.id"), nullable=False, default=str(uuid4())
    )
    tags = relationship("Tag", backref="post")

    def __repr__(self) -> str:
        return f"<Post id: {self.id}, title:{self.title}, content:{self.content}, timestamp:{self.timestamp}>"


class Category(Base):
    __tablename__ = "category"
    id = Column(String(64), primary_key=True, default=str(uuid4()))
    name = Column(String(64), unique=True, index=True)
    posts = relationship("Post", backref="category")
    tags = relationship(
        "Tag", secondary=tags, lazy="joined", backref=backref("categories", lazy=True)
    )

    def __repr__(self) -> str:
        return f"<Category id:{self.id}, name:{self.name}, tags:{self.tags}>"


class Tag(Base):
    __tablename__ = "tag"
    id = Column(String(64), primary_key=True, default=str(uuid4()))
    name = Column(String(64), unique=True, index=True)
    post_id = Column(String(64), ForeignKey("post.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Tag id:{self.id}, name:{self.name}, categories {self.categories}>"


# dummy table for many-to-many relationship between tag and category
tags = Table(
    "tags",
    Column("tag_id", String(64), ForeignKey("tag.id"), primary_key=True),
    Column("category_id", String(64), ForeignKey("category.id"), primary_key=True),
)
