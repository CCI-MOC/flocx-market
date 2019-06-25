from unittest import TestCase

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext import declarative
from sqlalchemy import Index

import alembic


class TestUnits(TestCase):
    def test_units(self):
        assert 5 * 5 == 25
