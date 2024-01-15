from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

import logging

# db_uri = 'postgresql://postgres:12345678@localhost/store'
db_uri = 'postgresql://iamjalgp:3LKSsKUu2in0JRB00flj5RsR0etCw2Ks@snuffleupagus.db.elephantsql.com/iamjalgp'
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(db_uri,pool_size=20, max_overflow=20, pool_pre_ping=True))
session = scoped_session(Session)


#recreate session
def recreate_session():
    try:
        logging.error('Try to recreate session ...')
        global Session
        Session = sessionmaker(autocommit=False,
                               autoflush=False,
                               bind=create_engine(db_uri, pool_size=20, max_overflow=20))
        global session
        session = scoped_session(Session)
        logging.error('Recreate session ... COMPLETED')
    except Exception as e:
        logging.error('WARNING SESSION RECREATE FAILED {0}'.format(e))
