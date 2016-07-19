#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 Peng Liu <myme5261314@gmail.com>
#
# Distributed under terms of the gplv3 license.

"""
Some utility functions.
"""

from company import Company
from bs4 import BeautifulSoup

def get_largest_duns_stored(session):
    """
    this function returns the largest valid duns stored in the database.
    """
    result = session.query(Company).order_by(Company.duns_id.desc())
    if result.count() == 0:
        return -1
    else:
        return result.one().duns_id


def get_next_duns(start=int(1e9)):
    if start == -1:
        start = int(1e9)
    # for num in range(start, int(1e10)):
    for num in range(start, int(start+200)):
        yield num



def handle_page(page):
    soup = BeautifulSoup(page)
    company_name = soup.findAll("span", class_="company")
    if company_name:
        company_name = company_name[0].h2.text
    company_addr = soup.findAll("span", class_="search_results_address")
    if company_addr:
        company_addr = company_addr[0].text.strip().split("\r\n")
