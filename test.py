#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 12:42:47 2017

@author: Anders
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:52:37 2017

@author: Anders

CAUTION: This must start with a blank table! 
        There is no protection against duplicates!
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import Variant, Read, Stats

# SQL setup
Base = declarative_base()
#engine = create_engine('mysql+pymysql://root@localhost:3306/cpd', echo=False)
engine = create_engine('sqlite:///CPD.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()





variants = session.query(Read.var_id).filter_by(sample = 'CPDC151823').first()