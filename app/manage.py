from sqlalchemy import create_engine
from models import Base, Product, Position

# Use the ElephantSQL URI
db_uri = 'postgresql://iamjalgp:3LKSsKUu2in0JRB00flj5RsR0etCw2Ks@snuffleupagus.db.elephantsql.com/iamjalgp'
engine = create_engine(db_uri)

# Create tables
Base.metadata.create_all(bind=engine)
