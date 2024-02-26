from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from faker import Faker

from api import models
from api.db import get_db


router = APIRouter()


class PostsViewModel(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[PostsViewModel])
def list_posts(user_id: int = None, db: Session = Depends(get_db)):
    posts_query = db.query(models.Post)
    if user_id is not None:
        posts_query = posts_query.filter(models.Post.user_id == user_id)
    return posts_query.all()


class PostAddViewModel(BaseModel):
    title: str
    content: str
    user_id: int


@router.post("/", response_model=PostsViewModel)
def add_post(post: PostAddViewModel, db: Session = Depends(get_db)):
    user = db.query(models.User).get(post.user_id)
    if not user:
        raise HTTPException(400)

    post = models.Post(title=post.title, content=post.content, user_id=user.id)
    db.add(post)
    db.commit()

    return post


@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(404)

    post.like += 1
    db.commit()


class CommentsViewModel(BaseModel):
    id: int
    name: str
    body: str

    class Config:
        from_attributes = True


class CommentAddViewModel(BaseModel):
    name: str
    body: str


class TagsViewModel(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TagAddViewModel(BaseModel):
    name: str


class PostDetailsViewModel(BaseModel):
    id: int
    title: str
    content: str
    like: int
    comments: List[CommentsViewModel]
    tags: List[TagsViewModel]

    class Config:
        from_attributes = True


@router.post("/{post_id}/comment", response_model=CommentsViewModel)
def create_comment(post_id: int, comment: CommentAddViewModel, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(404)

    comment = models.Comment(name=comment.name, body=comment.body, post_id=post.id)
    db.add(comment)
    db.commit()

    return comment


def get_pagination_params(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
):
    return {"offset": offset, "limit": limit}


@router.get("/{post_id}", response_model=PostDetailsViewModel)
def get_post(
        response: Response,
        post_id: int, db: Session = Depends(get_db),
        pagination: dict = Depends(get_pagination_params)):

    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(404)

    offset = pagination["offset"]
    limit = pagination["limit"]
    comments = db.query(models.Comment)\
        .filter(models.Comment.post_id == post_id)\
        .order_by(models.Comment.id.desc())\
        .slice(offset, limit)\
        .all()

    comments_view = [CommentsViewModel(id=comment.id, name=comment.name, body=comment.body) for comment in comments]
    response.headers["Comments-Total-Count"] = str(len(comments_view))
    response.headers["Comments-Offset"] = str(offset)
    response.headers["Comments-Limit"] = str(limit)

    tags = db.query(models.Tag).filter(models.Tag.post_id == post_id).all()
    tags_view = [TagsViewModel(id=tag.id, name=tag.name) for tag in tags]

    post = PostDetailsViewModel(
        id=post.id,
        title=post.title,
        content=post.content,
        like=post.like,
        comments=comments_view,
        tags=tags_view
    )

    return post


@router.post("/{post_id}/faker")
def generate_fake_comments(post_id: int, number: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(404, detail="Post not found")

    fake = Faker()
    fake_comments = []

    for i in range(number):
        name = fake.name()
        body = fake.paragraphs(nb=1)[0]
        comment = models.Comment(name=name, body=body, post_id=post.id)
        fake_comments.append(f'Comment no. {i + 1} = "{body}" by {name}')
        db.add(comment)

    db.commit()

    return fake_comments


@router.post("/{post_id}/tag", response_model=TagsViewModel)
def create_tag(post_id: int, tag: TagAddViewModel, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    if not post:
        raise HTTPException(404)

    tag = models.Tag(name=tag.name, post_id=post.id)
    db.add(tag)
    db.commit()

    return tag
