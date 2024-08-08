from .db import Session
from .models import Match
from app.logger import logger


session = Session()


def add_match(matct_data):
    with Session() as session:
        with session.begin():
            m = Match(**matct_data.dict())
            session.add(m)
            logger.info(f"{m} push to DB")
