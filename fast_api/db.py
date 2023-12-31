import os
from typing import Optional

import cv2
from sqlalchemy import ForeignKey, create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy_utils import create_database, database_exists, drop_database

from configs.main_config import images_after_treatment, images_before_treatment
from configs.postgre_config import (posgres_user, posgres_user_password,
                                    sql_alchemy_engine)


class Base(DeclarativeBase):
    pass


class Image(Base):
    __tablename__ = "image"

    image_id: Mapped[int] = mapped_column(primary_key=True)
    image_before_treatment: Mapped[Optional[str]]
    image_after_treatment: Mapped[Optional[str]]


class Car(Base):
    __tablename__ = "car"

    car_id: Mapped[int] = mapped_column(primary_key=True)
    x1: Mapped[float] = mapped_column()
    y1: Mapped[float] = mapped_column()
    x2: Mapped[float] = mapped_column()
    y2: Mapped[float] = mapped_column()
    score: Mapped[Optional[float]]
    type: Mapped[Optional[str]]
    image_id: Mapped[int] = mapped_column(
        ForeignKey("image.image_id", ondelete="CASCADE")
    )


class License_plate(Base):
    __tablename__ = "license_plate"

    lp_id: Mapped[int] = mapped_column(primary_key=True)
    x1: Mapped[float] = mapped_column()
    y1: Mapped[float] = mapped_column()
    x2: Mapped[float] = mapped_column()
    y2: Mapped[float] = mapped_column()
    score: Mapped[Optional[float]]
    text: Mapped[Optional[str]]
    type: Mapped[Optional[str]]
    car_id: Mapped[int] = mapped_column(ForeignKey("car.car_id", ondelete="CASCADE"))


def get_engine():
    return create_engine(sql_alchemy_engine)


def get_session():
    return Session(get_engine())


def add_image(image_np, image_name):
    session = get_session()

    bp = os.path.join(os.getcwd(), images_before_treatment, image_name)
    ap = os.path.join(os.getcwd(), images_after_treatment, image_name)
    image = Image(image_before_treatment=bp, image_after_treatment=ap)

    redundant_images = delete(Image).where(Image.image_before_treatment == bp)
    redundant_images = session.execute(redundant_images)
    session.commit()
    session.add(image)
    session.commit()
    cv2.imwrite(bp, image_np)
    return image.image_id


def add_car(boxes, image_id, scores=[None], types=[None]):
    session = get_session()

    assert len(boxes) == len(scores)
    assert len(boxes) == len(types)

    car_ids = []

    for i in range(len(boxes)):
        # try:
        # car = Car(
        #     x1=boxes[i][0].item(),
        #     y1=boxes[i][1].item(),
        #     x2=boxes[i][2].item(),
        #     y2=boxes[i][3].item(),
        #     score=scores[i].item(),
        #     type=types[i],
        #     image_id=image_id,
        #     )
        # except:
        car = Car(
            x1=boxes[i][0].item(),
            y1=boxes[i][1].item(),
            x2=boxes[i][2].item(),
            y2=boxes[i][3].item(),
            score=scores[i],
            type=types[i],
            image_id=image_id,
        )
        session.add(car)
        session.commit()
        car_ids.append(car.car_id)
    return car_ids


def add_lp(boxes, score, types, texts, car_id):
    session = get_session()

    lp_ids = []
    for i in range(len(boxes)):
        lp = License_plate(
            x1=boxes[i][0].item(),
            y1=boxes[i][1].item(),
            x2=boxes[i][2].item(),
            y2=boxes[i][3].item(),
            score=score[i].item(),
            type=types[i],
            text=texts[i],
            car_id=car_id,
        )
        session.add(lp)
        session.commit()
        lp_ids.append(lp.lp_id)
    return lp_ids


def get_lp_and_cars_by_image(image_id):
    session = get_session()
    stmt = select(Car).where(Car.image_id == image_id)
    cars = session.execute(stmt).fetchall()[0]
    lp_bboxes = []
    lp_types = []
    lp_texts = []
    for car_id in [x.car_id for x in cars]:
        stmt = select(License_plate).where(License_plate.car_id == car_id)
        lps = session.execute(stmt).fetchall()[0]
        lp_bboxes.extend(
            [
                x.x1,
                x.y1,
                x.x2,
                x.y2,
            ]
            for x in lps
        )
        lp_types.extend([x.type for x in lps])
        lp_texts.extend([x.text for x in lps])
    return (
        lp_bboxes,
        lp_types,
        lp_texts,
    )


def create_db():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)


def create_tables_in_db():
    engine = get_engine()
    Base.metadata.create_all(engine)


def drop_db():
    engine = get_engine()
    if database_exists(engine.url):
        drop_database(engine.url)


def get_db_user_credentials():
    return {
        "posgres_user": posgres_user,
        "posgres_user_password": posgres_user_password,
        "command": f"sudo -u postgres createuser --login --no-superuser --createdb --createrole -e {posgres_user} -P;",
    }
