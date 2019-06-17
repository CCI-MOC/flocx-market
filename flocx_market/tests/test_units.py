from unittest import TestCase

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative
from sqlalchemy import Index

import wsmeext.pecan as wsme_pecan
from pecan import hooks
from pecan import rest
from wsme import types as wtypes
from flocx_market.api.controllers.v1 import controller as v1_controller
from flocx_market.api import expose as ep
from pecan import request
from wsgiref import simple_server

import alembic

class TestUnits(TestCase):

    def test_units(self):
        assert 5 * 5 == 25
