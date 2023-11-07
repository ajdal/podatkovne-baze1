# Stikanje

```sql
SELECT stolpci
FROM tab1 
   [NATURAL] [LEFT | RIGHT | FULL ] JOIN tab2 [ON pogoj | USING (stolpci)]
WHERE pogoj
GROUP BY stoplci
HAVING pogoj
ORDER BY stolpci
LIMIT stevilo
```

* `ON pogoj` - poveže vrstice iz obeh tabel, kjer velja pogoj (npr. `ON oseba.id = vloga.oseba`)
* `USING` - stakne po istoimenskih stolpcih v obeh tabelah, ki jih navedemo (npr. `USING id`)
* `NATURAL JOIN` - stakne po vseh istoimenskih stolpcih v obeh tabelah. Pogoja stikanja potem ne navajamo.
* stikanje se izvede pred filtriranjem z `WHERE`!


## Različni tipi stikanja

Dano imamo podatkovno bazo naročil s tabelama `stranka` in `narocilo`.

Tabela `stranka`:
| id | ime    |
|----|--------|
| 1  | Alenka |
| 2  | Branko |
| 3  | Cvetka |
| 4  | David  |

Tabela `narocilo`:
| id | kolicina | stranka |
|----|----------|---------|
| 1  | 500      | 2       |
| 2  | 300      | 6       |
| 3  | 800      | 2       |
| 4  | 150      | 1       |
| 5  | 400      | 4       |

Povezati želimo količino naročenih izdelkov z imeni strank.

### Notranji stik (INNER JOIN)

Pridobiti želimo le vrstice, za katere poznamo vnos tako v levi, kot v desni tabeli.

```sql
SELECT *
FROM stranka
    JOIN narocilo ON stranka.id = narocilo.stranka
```

Če izberemo vse stolpce (`*`), poizvedba vrne vse stolpce iz prve (`stranka`), nato pa še vse stolpce iz druge tabele (`narocilo`), za vrstice, kjer se id stranke ujema s stolpcem stranka v tabeli `narocilo`:

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 2  | Branko | 2    | 500      | 2       |
| 2  | Branko | 4    | 800      | 2       |
| 1  | Alenka | 5    | 150      | 1       |
| 4  | David  | 5    | 400      | 4       |

V stavku `SELECT` lahko torej izberemo katerikoli stolpec iz te staknjene tabele.
Denimo, da želimo prikazati le ime stranke, id naročila in količino:

```sql
SELECT ime, narocilo.id as narocilo_id, kolicina
FROM stranka
    JOIN narocilo ON stranka.id = narocilo.stranka
```
Poizvedba vrne naslednji rezultat:

| ime    | narocilo_id | kolicina |
|--------|------|----------|
| Branko | 2    | 500      |
| Branko | 4    | 800      |
| Alenka | 5    | 150      |
| David  | 5    | 400      |

Ker se stolpec `id` nahaja tako v tabeli stranka, kot v tabeli narocilo, moramo v povedati, iz katere tabele želimo pridobiti stolpec `id` -> `narocilo.id`.

### Zunanji stik (OUTER JOIN)

Ločimo tri vrste zunanjih stikov.

**Levi zunanji stik** (LEFT OUTER JOIN) ohrani vse vrstice iz prve tabele - vse stranke:

```sql
SELECT *
FROM stranka
    LEFT JOIN narocilo ON stranka.id = narocilo.stranka
```

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 1  | Alenka | 5    | 150      | 1       |
| 2  | Branko | 2    | 500      | 2       |
| 2  | Branko | 4    | 800      | 2       |
| 3  | Cvetka | NULL | NULL     | NULL    |
| 4  | David  | 5    | 400      | 4       |

Ker Cvetka ni opravila nobenega naročila, stolpci iz desne tabele (`narocilo`) dobijo vrednost `NULL`.

**Desni zunanji stik** (RIGHT OUTER JOIN) ohrani vse vrstice iz druge tabele - vsa naročila:

```sql
SELECT *
FROM stranka
    RIGHT JOIN narocilo ON stranka.id = narocilo.stranka
```

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 1     | Alenka    |	4 |	150 | 1 |
| 2     | Branko    |	1 |	500 | 2 |
| 2     | Branko    |	3 |	800 | 2 |
| 4     | David     |	5 |	400 | 4 |
| NULL  | NULL      |	2 |	300 | 6 |

Opazimo, da se ohrani vrstni red iz leve tabele.

**Polni zunanji stik** (FULL OUTER JOIN) ohrani vse vrstice iz obeh tabel:

```sql
SELECT *
FROM stranka
    FULL JOIN narocilo ON stranka.id = narocilo.stranka
```

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 1  | Alenka | 5    | 150      | 1       |
| 2  | Branko | 2    | 500      | 2       |
| 2  | Branko | 4    | 800      | 2       |
| 3  | Cvetka | NULL | NULL     | NULL    |
| 4  | David  | 5    | 400      | 4       |
 NULL| NULL   |	2    | 300      | 6       |

## Primeri z bazo `filmi`

1. Naslovi filmov in imena glavnih igralcev (urejeno po imenih, nato pa po naslovih).

* Tabela `vloga` povezuje igralce in režiserje iz tabele `oseba` s filmi iz tabele `film` .
* Staknemo vrstice z istim id filma in id osebe.
* Tip vloge mora biti `'I'`.
* Mesto vloge mora biti 1.

```sql
SELECT naslov, ime
FROM film
    JOIN vloga ON film.id = vloga.film
    JOIN oseba ON oseba.id = vloga.oseba
WHERE tip = 'I' AND mesto = 1
ORDER BY ime, naslov
```

_Ker so ime, naslov, tip in mesto prisotni vsak le v eni tabeli, nam imena tabele ni treba podati ob imenu stolpca. Stolpec id se pojavi tako v tabeli film, kot v tabeli oseba, zato smo ju zapisali kot `film.id` in `oseba.id`_

2. Za vsakega režiserja (izpišite ga z IDjem in imenom) izpišite skupno dolžino filmov, ki jih je režiral (brez igranja). Rezultate uredite po imenu režiserja.

* Staknemo tabele `oseba`, `vloga`, `film` po IDjih.
* Izberemo le vrstice, kjer je tip enak `'R'` (režiser) - to moramo storiti pred združevanjem.
* Združimo po id in imenu osebe - v `SELECT` imamo lahko le stolpce, po katerih združujemo in agregirane stolpce (`SUM`, `MIN`, `MAX`, ...).
* Uredimo.

```sql
SELECT oseba.id, ime, SUM(film.dolzina)
FROM oseba
    JOIN vloga on oseba.id = vloga.oseba
    JOIN film on vloga.film = film.id
WHERE vloga.tip = 'R'
GROUP BY oseba.id, ime
ORDER BY ime
```

3. Za vsak žanr (izpišite ga z imenom) izpišite število različnih igralcev in število različnih režiserjev, ki so sodelovali pri filmih tega žanra. Rezultate uredite padajoče po vsoti števila igralcev in števila režiserjev (če se nekdo pojavi tako kot igralec kot režiser, se tukaj šteje dvakrat).

* Sestaviti moramo seznam igralcev in seznam režiserjev za vsak žanr, nato pa prešteti le različne za vsako vlogo.
* Tabele oseba tu ne potrebujemo, ker nas ne zanimajo imena, ampak le število.
* Stakniti bo treba tabele `film`, `pripada` in `zanr`, da bomo lahko združili filme po žanrih in izpisali nazive žanrov.
* Ločeno bomo morali poiskati igralce in režiserje (osebe z dvojno vlogo se štejejo k obema vlogama). To lahko storimo na dva načina:
    1. Ustvarimo vse pare vlog za posamezen film, nato izberemo le ustrezne.
    2. Ločeno naredimo gnezdeni poizvedbi za igralce in režiserje.


1. Ustvarimo pare vlog:

* Vse skupaj staknemo z dvema kopijama tabele `vloga` - eno vlogo imenujno `igralec`, drugo pa `reziser`.
* Tabele staknemo po id filma.
* Dobimo **vse** pare oseb, ki so sodelovale pri istem filmu.
* Sedaj moramo poskrbeti, da bodo v eni kopiji ostali le igralci, v drugi pa le režiserji - tabelo filtriramo z `WHERE` tako, da bo stolpec `tip` iz tabele `igralec` enak `'I'`, `tip` iz tabele `reziser` pa `'R'`.
* Dobimo vse pare oblike (igralec, reziser) za posamezen film.
* Ker nas zanimajo podatki za posamezne žanre, jih združimo po žanrih.
* Preštejemo število **različnih** igralcev in število **različnih** režiserjev, ter vrednostima priredimo ime (`AS stevilo_igralcev`), da se lahko pri urejanju sklicujemo nanju.
* Uredimo po vsoti obeh vrednosti.

```sql
SELECT naziv,
    COUNT(DISTINCT igralec.oseba) AS stevilo_igralcev,
    COUNT(DISTINCT reziser.oseba) AS stevilo_reziserjev FROM film
  JOIN pripada ON film.id = pripada.film
  JOIN zanr ON pripada.zanr = zanr.id
  JOIN vloga AS igralec ON film.id = igralec.film
  JOIN vloga AS reziser ON film.id = reziser.film
WHERE igralec.tip = 'I' AND reziser.tip = 'R'
GROUP BY zanr.id, naziv
ORDER BY stevilo_igralcev + stevilo_reziserjev DESC;
```