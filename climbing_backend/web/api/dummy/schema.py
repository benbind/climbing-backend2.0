from pydantic import BaseModel


class ClimberCreate(BaseModel):
    name: str
    photo: str
    highest_grade: int


class ClimberRead(ClimberCreate):
    id: int


class PostCreate(BaseModel):
    video: str
    caption: str
    climb_id: int
    climber_id: int


class PostRead(PostCreate):
    id: int


class LocationCreate(BaseModel):
    name: str
    number_of_climbs: int
    latlon: str
    is_indoor: bool


class LocationRead(LocationCreate):
    id: int


class ClimbCreate(BaseModel):
    name: str
    grade: int
    location_id: int


class ClimbRead(ClimbCreate):
    id: int


class CommentCreate(BaseModel):
    post_id: int
    climber_id: int
    text: str


class CommentRead(CommentCreate):
    id: int
