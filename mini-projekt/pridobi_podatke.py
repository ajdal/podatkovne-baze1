import requests
import bs4

def pridobi_ime(blok):
    ime = blok.find_all("div", attrs={"class": "product__teaser__title"})[0]
    return ime.h2.string

def pridobi_ceno(blok):
    podatki = blok.find_all("div", attrs={"class": "product__teaser__price"})[0]
    cena = float(podatki.div.span.string)
    valuta = podatki.div.next.next_sibling.next_sibling.next_sibling.string
    return cena, valuta

odgovor = requests.get("https://www.legendww.me/zenska-odjeca")
juha = bs4.BeautifulSoup(odgovor.content)
with open("podatki/oblacila.csv", "w", encoding="utf8") as dat:
    print("ime,cena,valuta", file=dat)
    for izdelek in juha.find_all("div", attrs={"class": "product__teaser"}):
        ime = pridobi_ime(izdelek)
        cena, valuta = pridobi_ceno(izdelek)
        print(f"{ime},{cena},{valuta}", file=dat)
