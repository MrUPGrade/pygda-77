from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), default=False, nullable=False)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    like = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")
    post_comment = relationship("Comment", back_populates="post_related")
    post_tag = relationship("Tag", back_populates="post_related")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    body = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post_related = relationship("Post", back_populates="post_comment")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post_related = relationship("Post", back_populates="post_tag")
