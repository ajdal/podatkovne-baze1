# Ustvarjanje tabel

```sql
CREATE TABLE tabela (
    stolpec tip 
        [PRIMARY KEY]                   -- stolpec je glavni ključ tabele
        [NOT NULL]                      -- vrednost stolpca ne sme biti NULL
        [UNIQUE]                        -- vrednosti v stolpcu se ne smejo ponavljati
        [CHECK (pogoj)]                 -- pogoj, ki mora veljati za vse vrednosti v stopcu
        [DEFAULT (vrednost)]            -- privzeta vrednost, ki se uporabi, če vrednosti ne podamo ob vstavljanju
        [REFERENCES tabela2(stolpec2)]  -- tuji ključ: vredost stolpca povezuje tabelo s tabelo tabela2 preko stolpca stolpec2
        [AUTOINCREMENT]                 -- če vrednost stolpca ni podana, se avtomatsko uporabi za eno večja vrednost od prej največje
    [PRIMARY KEY (st1, st2, ...)]       -- glavni ključ tabele je sestavljen iz več stolpcev
    [UNIQUE (st1, st2, ...)]            -- kombinacija vrednosti v stolpcih se ne sme ponavljati
    [CHECK (pogoj)]                     -- pogoj, ki vključuje več stolpcev
    [FOREIGN KEY (st1, st2, ...)] REFERENCES tabela2(s1, s2, ...) -- tuji ključ je sestavljen iz več stolpcev
    ...
);
```
Določila v oglatih oklepajih so opcijska. Nabor in imena določil se lahko razlikujejo med različnimi tipi podatkovnih baz (RDMBS - npr. SQLite, MySQL, PostgreSQL, MariaDB, Microsoft SQL Server, Oracle Database, ...).

Opomba: Določilo `PRIMARY KEY` vključuje pogoj `NOT NULL` ter avtomatsko poskrbi za prirejanje/povečevanje vrednosti, če ta ni podana, zato določilo `AUTOINCREMENT` ni potrebno. ([več o tem](https://www.sqlitetutorial.net/sqlite-primary-key/))

Tipi v `SQLite`:
* `integer` - celo ševilo
* `real`, `numeric(p, s)`, `decimal(p, s)` - decimalno število
* `text` - niz
* `char(n)`, `varchar(n)` - omejena dolžina niza
* `date` - datum (`YYYY-MM-DD`)
* `time` - čas (`hh:mm:ss`)
* `datetime` - datum in čas (`YYYY-MM-DD hh:mm:ss`)

## Ustvarjanje baze 

Odprite program SQLite Studio, kjer boste ustvarili bazo z učitelji.

1. Dodajte novo bazo (napišite ime še neobstoječe datoteke) in odprite urejevalnik stavkov SQL.
2. Naredite tabelo ucitelji, ki naj ima stolpce id, ime, priimek in email. Stolpec id naj bo tipa integer, ostali stolpci pa tipa text. Stolpec id naj bo glavni ključ tabele.

```sql
CREATE TABLE ucitelji (
    id integer PRIMARY KEY,
    ime text,
    priimek text,
    email text
);
```

3. Naredite tabelo predmeti, ki naj vsebuje stolpce id, ime in ects. Stolpca id in ects naj bosta tipa integer, ime predmeta pa text. Spet naj bo stolpec id glavni ključ tabele.

```sql
CREATE TABLE predmeti (
    id integer PRIMARY KEY,
    ime text,
    ects integer
);
```

4. V tabeli ucitelji smo pozabili na stolpec kabinet. Tabelam lahko dodajamo stolpce na naslednji način: ALTER TABLE ime_tabele ADD COLUMN ime_stolpca tip_stolpca; Tip stolpca naj bo kar text, saj oznaka kabineta lahko vsebuje tudi piko in črke.

```sql
ALTER TABLE ucitelji
ADD COLUMN kabinet text;
```

5. Naredite še šifrant vlog, in sicer kot tabelo vloge, ki ima stolpca id (tipa integer) in opis (tipa text). Poskrbi tudi za glavni ključ. Vloga z id 0 ustreza predavateljem, vloga 1 pa, da gre za asistenta.

```sql
CREATE TABLE vloge (
    id integer PRIMARY KEY,
    opis text
);
```

6. Naredite tabelo izvajalci, ki naj ima tri stolpce (vsi so tipa integer): idpredmeta, iducitelja in vloga. Poskrbi za ustrezne reference na ostale tabele.

```sql
CREATE TABLE izvajalci (
    idpredmeta integer REFERENCES predmeti(id),
    iducitelja integer REFERENCES ucitelji(id),
    vloga integer REFERENCES vloge(id)
);
```


7. Napolnite tabele ucitelji, predmeti, vloge in izvajalci s stavki `INSERT` v datotekah na spletni učilnici. Da ne bo potrebno izvajati vsakega stavka posebej, v SQLite Studiu pritisnite F10 in odstranite kljukico pri `Execute only the query under the cursor`.

Napišite naslednje poizvedbe:

1. Naredite poizvedbo, ki poišče najbolj zasedene kabinete.

* Najprej z `WHERE` izberemo le vrstice, kjer je kabinet znan, da se izognemo skupini `NULL`.
* Zaposlene združimo po kabinetih. 
* Uredimo padajoče po številu učiteljev v kabinetu.

```sql
SELECT kabinet, COUNT(*) as st_uciteljev
FROM ucitelji
WHERE kabinet IS NOT NULL
GROUP BY kabinet
ORDER BY st_uciteljev DESC;
```

2. Naredite poizvedbo, ki bo prikazala vse pare cimrov. Izpisati je treba tabelo, ki ima 4 stolpce (ime1, priimek1, ime2, priimek2). Za vsaka dva učitelja, ki si delita pisarno, se mora v rezultatu pojaviti po ena vrstica.

* Tabelo učiteljev staknemo samo s sabo, da lahko dobimo pare učiteljev.
* Povežemo vrstice, kjer se ujema oznaka kabineta
* Uporabimo pogoj, da je `id` prvega učitelja manjši od `id` drugega učitelja - s tem izločimo podvojene vrstice, kjer sta cimra zapisana v obratnem vrstnem redu, ter vrstice, ki pravijo, da je učitelj sam svoj cimer. 

```sql
SELECT u1.ime AS ime1, u1.priimek AS priimek1, u2.ime AS ime2, u2.priimek AS priimek2
FROM ucitelji AS u1
    JOIN ucitelji AS u2 ON u1.kabinet = u2.kabinet
WHERE u1.id < u2.id;
```

3. Naredite poizvedbo, ki bo vrnila tabelo vseh trojic predmet-učitelj-asistent. Iz te tabele se bo dalo razbrati, pri kolikih predmetih sodelujeta nek učitelj in asistent.

```sql
SELECT predmeti.ime, predavatelji.ime || ' ' || predavatelji.priimek AS predavatelj, asistenti.ime || ' ' || asistenti.priimek AS asistent
FROM izvajalci AS iz1
    JOIN izvajalci AS iz2 ON iz1.idpredmeta = iz2.idpredmeta
    JOIN predmeti ON iz1.idpredmeta = predmeti.id
    JOIN ucitelji AS predavatelji ON iz1.iducitelja = predavatelji.id
    JOIN ucitelji AS asistenti ON iz2.iducitelja = asistenti.id
WHERE predavatelji.id != asistenti.id AND iz1.vloga = 0 AND iz2.vloga=1;
```