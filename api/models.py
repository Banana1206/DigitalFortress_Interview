from database import Base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey,  LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(length=32), nullable=False, unique=True, index=True)
    password: str = Column(String(length=64), nullable=False)
    email: str = Column(String(length=64), nullable=True, unique=True)

class Island(Base):
    __tablename__ = "islands"
    
    island_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    area = Column(Float)
    description = Column(Text)


class Comment(Base):
    __tablename__ = "comments"
    
    comment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    island_id = Column(Integer, ForeignKey("islands.island_id"))
    image_id = Column(Integer, ForeignKey("images.image_id"))
    content = Column(Text)
    

class Image(Base):
    __tablename__ = "images"
    
    image_id = Column(Integer, primary_key=True, index=True)
    image = Column(LargeBinary)
    caption = Column(Text, nullable=True)


class Video(Base):
    __tablename__ = "videos"
    
    video_id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.comment_id"))
    video_url = Column(String)
    caption = Column(Text, nullable=True)

