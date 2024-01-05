from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from climbing_backend.db.base import Base
from climbing_backend.db.models.users import User  # type: ignore[attr-defined]


class Climber(Base):
    __tablename__ = "climbers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String)
    photo: Mapped[String] = mapped_column(String)
    highest_grade: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User")
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="climber")


class Climb(Base):
    __tablename__ = "climbs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String)
    grade: Mapped[int] = mapped_column(Integer)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"))
    location: Mapped["Location"] = relationship("Location")


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String)
    number_of_climbs: Mapped[int] = mapped_column(Integer)
    latlon: Mapped[int] = mapped_column(String)
    is_indoor: Mapped[bool] = mapped_column(Boolean)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[String] = mapped_column(String)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    climber_id: Mapped[int] = mapped_column(Integer, ForeignKey("climbers.id"))
    post: Mapped["Post"] = relationship("Post")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    video: Mapped[String] = mapped_column(String)
    caption: Mapped[String] = mapped_column(String)
    climb_id: Mapped[int] = mapped_column(Integer, ForeignKey("climbs.id"))
    climber_id: Mapped[int] = mapped_column(Integer, ForeignKey("climbers.id"))
    climber: Mapped[Climber] = relationship("Climber", back_populates="posts")
    climb: Mapped[Climb] = relationship("Climb")
