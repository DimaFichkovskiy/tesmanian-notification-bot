import sqlalchemy as db
import psycopg2
from sqlalchemy import create_engine, insert, select, desc
from sqlalchemy.ext.declarative import declarative_base

DB_URI = f'postgresql+psycopg2://admin:example@db:5432/tesmanian'

engine = create_engine(DB_URI)
Base = declarative_base(bind=engine)


class News(Base):
    __tablename__ = 'news'

    id = db.Column(db.INT(), primary_key=True)
    title = db.Column(db.String())
    url = db.Column(db.String())


class DBDriver:
    @classmethod
    def add_new_news(cls, title: str, url: str):
        with engine.connect() as conn:
            conn.execute(
                insert(News).values(
                    title=title,
                    url=url
                )
            )

    @classmethod
    def get_last_news(cls):
        with engine.connect() as conn:
            news = conn.execute(
                select(News.url).order_by(desc(News.id)).limit(11)
            )
            return news


if __name__ == '__main__':
    Base.metadata.create_all(engine)
