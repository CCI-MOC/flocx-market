import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext import declarative
from sqlalchemy import Index
import sqlalchemy_jsonfield
# declare a mapping
Base = declarative.declarative_base()

class Offer(Base):
	__tablename__ = 'offer'
	id = Column(Integer, primary_key=True, autoincrement=True)
	marketplace_offer_id = Column(String(64), nullable=False, unique=True)
	provider_id = Column(String(64), nullable=False, unique=True)
	creator_id = Column(String(64), nullable=False, unique=True) #username that created the offer
	marketplace_date_created = Column(DateTime(timezone=True), nullable=False)
	status = Column(String(15), nullable=False, default = 'available')
	server_name = Column(String(64), nullable=False, unique=True)
	start_time = Column(DateTime(timezone=True), nullable=False)
	end_time = Column(DateTime(timezone=True), nullable=False)
	duration = Column(Integer, nullable=False)
	server_config =  Column(sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False
        ),
        nullable=False)
	cost = Column(Integer, nullable=False)

# class Bid(Base):
# 	__tablename__ = 'bids'
# 	id = Column(Integer, primary_key=True, autoincrement=True)
# 	marketplace_id = Column(String(64), nullable=False, unique=True)
# 	creator_id = Column(String(64), nullable=False, unique=True)
# 	start_time = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
# 	Server_quantity = Column(Integer, nullable=False)
# 	end_time = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
# 	duration = Column(Integer, nullable=False)
# 	status = Column(Enum(statusEnum), nullable=False, default = statusEnum.available.value)
# 	server_config =  Column(sqlalchemy_jsonfield.JSONField(
#             # MariaDB does not support JSON for now
#             enforce_string=True,
#             # MariaDB connector requires additional parameters for correct UTF-8
#             enforce_unicode=False
#         ),
#         nullable=False)
# 	cost = Column(Integer, nullable=False)

