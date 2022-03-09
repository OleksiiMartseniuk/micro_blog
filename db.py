import databases
import sqlalchemy
import ormar


metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite:///blog.db")
engine = sqlalchemy.create_engine("sqlite:///blog.db")


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
