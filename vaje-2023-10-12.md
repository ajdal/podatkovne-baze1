# Osnove SQL

Oblika osnovne SQL poizvedbe:
```sql
SELECT stolpec1, stolpec2 AS ime_stolpca, stolpec3 / 1000, ROUND(stolpec4, 3), DISTINCT stolpec5
FROM tabela
WHERE stolpec1 = 'vrednost1' AND ime_stolpca LIKE '%vrednost_' OR stolpec3 / 1000 > 25
ORDER BY stolpec1 DESC; stolpec4
LIMIT 20
```

## Primeri z vaj z bazo `filmi`:

1. Izpišimo vse naslove filmov
```sql
SELECT naslov
FROM film
```

2. Izpišimo vse naslove, dolžine in ocene
```sql
SELECT naslov, dolzina, ocena
FROM film
```

3. Uredimo izpis padajoče po ocenah
```sql
SELECT naslov, dolzina, ocena
FROM film
ORDER BY ocena DESC
```

4. Zanimajo nas le filmi, ki so dolgi največ 2,5h
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina < 150
ORDER BY ocena DESC
```

5. A taki, ki niso krajši od 2h
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC
```

6. Zanima nas le prvih 20 takšnih filmov.
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC
LIMIT 20
```

7. Dodatno filme uredimo še naraščajoče po trajanju
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC, dolzina
LIMIT 20
```