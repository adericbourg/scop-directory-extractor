#!/usr/bin/env python3

import csv
from typing import List
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from helper import io
from helper.model import Scop

BASE_URL = 'https://www.les-scop-nouvelle-aquitaine.coop'


def run():
    content = _get_content()
    _write(content)


def _get_content() -> List[Scop]:
    page = 0
    content = []
    while True:
        page_content = _get_page(page)
        if not len(page_content):
            return content
        content.extend(page_content)
        page = page + 1


def _get_page(page: int) -> List[Scop]:
    urls = _fetch_urls(page)
    scops = []
    for detail_url in urls:
        details = _get_details(detail_url)
        scops.append(details)
    return scops


def _fetch_urls(page: int) -> List[str]:
    req = Request(f"{BASE_URL}/l-annuaire?page={page}",
                  headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    detail_urls = []
    for card in soup.findAll('article', attrs={'class': "card"}):
        for link in card.findAll('a', attrs={'class': 'more-link'}):
            detail_urls.append(link.get('href'))
    return detail_urls


def _get_details(detail_url) -> Scop:
    req = Request(f"{BASE_URL}/{detail_url}", headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, 'html.parser')

    return Scop(
        name=soup.find('h1').find('span').string,
        address=_build_address(soup),
        phone=_get_field(soup, 'field--name-field-telephone'),
        email=_get_field(soup, 'field--name-field-email'),
        website=_get_field(soup, 'field--name-field-url'),
        scope=soup.find('div', attrs={'class': 'field--name-field-secteur-activite-structure'}).find('div').string
    )


def _build_address(soup: BeautifulSoup) -> str:
    address_holder = soup.find('p', attrs={'class': 'address'})
    line1 = address_holder.find('span', attrs={'class': 'address-line1'})
    line2 = address_holder.find('span', attrs={'class': 'address-line2'})
    postcode = address_holder.find('span', attrs={'class': 'postal-code'})
    city = address_holder.find('span', attrs={'class': 'locality'})

    address = line1.string
    if line2 is not None and len(line2):
        address = f"{address}, {line2.string}"
    return f"{address}, {postcode.string} {city.string}"


def _get_field(soup: BeautifulSoup, field: str) -> str:
    field = soup.find('div', attrs={'class': field})
    if field:
        return field.string
    else:
        return ""


def _write(scops: List[Scop]) -> None:
    with open(io.SCOP_CSV, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['Nom', 'Secteur', 'Adresse', 'E-mail', 'Téléphone', "Site"])
        for scop in scops:
            writer.writerow([scop.name, scop.scope, scop.address, scop.email, scop.phone, scop.website])


if __name__ == "__main__":
    run()
