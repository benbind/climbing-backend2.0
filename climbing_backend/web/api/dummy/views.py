from typing import Any, List, Optional, Sequence

from fastapi import APIRouter
from fastapi.param_functions import Body, Depends

import climbing_backend.web.api.dummy.schema as schema
from climbing_backend.db.base import Base
from climbing_backend.db.dao.dao import GenericDAO
from climbing_backend.db.models.models import Climb, Climber, Comment, Location, Post


def get_class_from_name(model_name: str) -> Optional[list[type]]:
    model_classes = {
        "climber": [Climber, schema.ClimberCreate, schema.ClimberRead],
        "climb": [Climb, schema.ClimbCreate, schema.ClimbRead],
        "location": [Location, schema.LocationCreate, schema.LocationRead],
        "post": [Post, schema.PostCreate, schema.PostRead],
        "comment": [Comment, schema.CommentCreate, schema.CommentRead],
    }
    return model_classes.get(model_name.lower())


router = APIRouter()


# creation routes
@router.put("/create/{model_name}")
async def create_object(
    model_name: str,
    dto_data: dict = Body(...),  # type: ignore
    dao: GenericDAO = Depends(),
) -> None:
    classes = get_class_from_name(model_name)
    if classes is not None:
        model_class, create_dto_class, _ = classes
        dto_instance = create_dto_class(**dto_data)
        await dao.create_model(model_class, dto_instance)


# search by id
@router.get("/search/climb/{climb_id}", response_model=schema.ClimbRead)
async def climb_by_id(
    climb_id: int,
    dao: GenericDAO = Depends(),
) -> Optional[Base]:
    return await dao.get_model_by_id(Climb, climb_id)


@router.get("/search/climber/{climber_id}", response_model=schema.ClimberRead)
async def climber_by_id(
    climber_id: int,
    dao: GenericDAO = Depends(),
) -> Optional[Base]:
    return await dao.get_model_by_id(Climber, climber_id)


@router.get("/search/location/{location_id}", response_model=schema.LocationRead)
async def location_by_id(
    location_id: int,
    dao: GenericDAO = Depends(),
) -> Optional[Base]:
    return await dao.get_model_by_id(Location, location_id)


@router.get("/search/post/{post_id}", response_model=schema.PostRead)
async def post_by_id(
    post_id: int,
    dao: GenericDAO = Depends(),
) -> Optional[Base]:
    return await dao.get_model_by_id(Post, post_id)


# deletion


@router.delete("/delete/climber/{climber_id}")
async def delete_climber_by_id(
    climber_id: int,
    dao: GenericDAO = Depends(),
) -> None:
    await dao.delete_model(Climber, climber_id)


@router.delete("/delete/post/{post_id}")
async def delete_post_by_id(
    post_id: int,
    dao: GenericDAO = Depends(),
) -> None:
    await dao.delete_model(Post, post_id)


@router.delete("/delete/climb/{climb_id}")
async def delete_climb_by_id(
    climb_id: int,
    dao: GenericDAO = Depends(),
) -> None:
    await dao.delete_model(Climb, climb_id)


@router.delete("/delete/location/{location_id}")
async def delete_location_by_id(
    location_id: int,
    dao: GenericDAO = Depends(),
) -> None:
    await dao.delete_model(Location, location_id)


@router.delete("/delete/comment/{comment_id}")
async def delete_comment_by_id(
    comment_id: int,
    dao: GenericDAO = Depends(),
) -> None:
    await dao.delete_model(Comment, comment_id)


# search by keyword
@router.get("/search_climb/{keyword}", response_model=List[schema.ClimbRead])
async def search_climb(
    keyword: str,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_model_by_name(Climb, keyword)


@router.get("/search_location/{keyword}", response_model=List[schema.LocationRead])
async def search_location(
    keyword: str,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_model_by_name(Location, keyword)


@router.get("/search_climber/{keyword}", response_model=List[schema.ClimberRead])
async def search_user(
    keyword: str,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_model_by_name(Climber, keyword)


# climbs in a location
@router.get("/location/{location_id}", response_model=List[schema.ClimbRead])
async def get_climbs_by_location(
    location_id: int,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_climbs_by_location(location_id)


# posts by climber
@router.get("/climber/{climber_id}", response_model=List[schema.PostRead])
async def get_posts_by_climber(
    climber_id: int,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_posts_by_climber(climber_id)


# comments by post
@router.get("/post/{post_id}", response_model=List[schema.CommentRead])
async def get_comments_by_post(
    post_id: int,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_comments_by_post(post_id)


# posts by climb
@router.get("/climb/{climb_id}", response_model=List[schema.PostRead])
async def get_posts_by_climb(
    climb_id: int,
    dao: GenericDAO = Depends(),
) -> Sequence[Any]:
    return await dao.get_posts_by_climb(climb_id)
