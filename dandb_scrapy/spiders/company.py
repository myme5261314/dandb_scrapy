#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Peng Liu <myme5261314@gmail.com>
#
# Distributed under terms of the gplv3 license.

"""
This file defines the class to operate with mysql via SQLAlchemy.
"""


from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = "duns_company"

    duns_id = Column(Integer, primary_key=True)
    company_name = Column(String)
    address = Column(String)
    country_code = Column(String)
    city = Column(String)
    postal_code = Column(String)
