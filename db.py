import databases
import ormar
import sqlalchemy


metadata = sqlalchemy.MetaData()
database = databases.Database("sqlite:///blog.db")
engine = sqlalchemy.create_engine("sqlite:///blog.db")


class BaseMata(ormar.ModelMeta):
    metadata = metadata
    database = database
