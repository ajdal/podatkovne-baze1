# Združevanje in podpoizvedbe

Združevanje
```sql
SELECT stolpec1, SUM(stolpec3), COUNT(stolpec2)
FROM tabela
WHERE stolpec1 LIKE '% %'
GROUP BY stolpec1, stolpec5
HAVING MIN(stolpec4) > 10
```

* `SUM`, `COUNT`, `MIN`, `MAX`, `AVG` - **združevalne funkcije**. Za več vrstic vrnejo 1 vrednost.
* `GROUP BY` - združi vse vrstice z isto vrednostjo danega stolpca oz. stolpcev v skupino.
* `HAVING` - **po združevanju** filtrira skupine glede na pogoj.

Pomembno:

* V `SELECT` in `HAVING` lahko direktno uporabimo le stolpce, po katerih smo združili poizvedbo (v zgornjem primeru `stolpec1`). Ostale stolpce moramo najprej "agregirati", da dobimo 1 vrednost za vsako skupino (vrednost stolpca `stolpec1`).
* `WHERE` filtrira vrstice **preden** jih združimo z `GROUP BY`. Za filtriranje po združenih vrednostih uporabimo `HAVING`.

## Primeri na bazi `filmi`:

1. Vrnite povprečno oceno filmov iz leta 2019.

```sql
SELECT AVG(ocena)
FROM film
WHERE leto = 2019
```

2. Za vsak ID osebe vrnite število različnih filmov, pri katerih je sodelovala ta oseba (bodisi kot igralec ali režiser). Ne izpisujte imen oseb.

```sql
SELECT oseba, COUNT(DISTINCT film) AS 'stevilo_filmov'
FROM vloga
GROUP BY oseba
```

3. Vrnite oznake, ki se pojavijo pri vsaj 100 filmih. Prazno oznako (NULL) izpustite.

```sql
SELECT oznaka, COUNT(*)
FROM film
WHERE oznaka NOT NULL -- odstrani vrstice, kjer je oznaka NULL
GROUP BY oznaka
HAVING COUNT(*) >= 100
```
ali
```sql
SELECT oznaka, COUNT(*)
FROM film
GROUP BY oznaka
HAVING COUNT(oznaka) >= 100 -- če štejemo samo po stolpcu oznaka, count ignorira vrstice z NULL
```

