# Spreminjanje podatkov v tabelah

### Dodajanje podatkov

```sql
todo
```

### Spreminjanje podatkov

```sql
todo
```

### Brisanje podatkov

```sql
todo
```

## Primeri

Preverimo izvajalce predmeta Podatkovne baze 1 in popravimo na trenutno stanje:
 
* Matija Pretnar ni več predavatelj pri predmetu PB1
* Janoš Vidali je predavatelj in ne več asistent
* Ajda Lampe je nova asistentka pri predmetu (in je še ni v tabeli učiteljev)


```sql

-- Izpišemo izvajalce
SELECT ucitelji.ime, ucitelji.priimek, predmeti.ime as predmet, vloge.opis FROM izvajalci
JOIN ucitelji ON ucitelji.id = iducitelja
JOIN predmeti ON predmeti.id = idpredmeta
JOIN vloge ON vloge.id = izvajalci.vloga
WHERE predmeti.ime = 'Podatkovne baze 1';

-- Odstranimo vrstico s predavateljem Matijo Pretnarjem
DELETE FROM izvajalci
WHERE (idpredmeta, iducitelja, vloga) = (SELECT iz1.idpredmeta, iz1.iducitelja, iz1.vloga FROM izvajalci AS iz1
JOIN ucitelji ON ucitelji.id = iducitelja
JOIN predmeti ON predmeti.id = idpredmeta
WHERE predmeti.ime = 'Podatkovne baze 1' AND vloga = 0);

-- Spremenimo, da bo Janoš Vidali predavatelj
UPDATE izvajalci
SET vloga = 0
WHERE (idpredmeta, iducitelja) = 
(SELECT iz.idpredmeta, iz.iducitelja
FROM izvajalci iz
    JOIN ucitelji ON ucitelji.id = iz.iducitelja
    JOIN predmeti ON predmeti.id = iz.idpredmeta
WHERE predmeti.ime = 'Podatkovne baze 1' AND iz.vloga = 1);
-- Tu smo se zanašali na to, da je bil to edini asistent pri predmetu. Če bi bilo asistentov več, bi filtrirali še po imenu in priimku.

-- Dodamo Ajdo Lampe
INSERT INTO ucitelji
(ime, priimek, email, kabinet)
VALUES ('Ajda', 'Lampe', 'ajda.lampe@fmf.uni-lj.si', 'M427');

-- Nastavimo Ajdo kot asistentko pri predmetu PB1
INSERT INTO izvajalci
(idpredmeta, iducitelja, vloga)
VALUES (
    (SELECT id FROM predmeti WHERE ime = 'Podatkovne baze 1'),
    (SELECT id FROM ucitelji WHERE ime = 'Ajda' AND priimek = 'Lampe'),
    1
);
    
```

## Naloge z vaj

Sledi nekaj nalog z bazo filmi (ena tabela), ki je podana na spletni učilnici.

### Dodajanje podatkov 1
V tabelo dodaj vsaj 5 filmov, posnetih po letu 2017. To naredi z enim ukazom `INSERT INTO`.


### Dodajanje podatkov 2
Denimo, da smo posneli novo različico vseh filmov, posnetih pred letom 1950 s certifikatom G, PG ali PG-13. Vstavi jih v tabelo, z ustrezno popravljenim naslovom, opisom in režiserjem. Njihova dolžina naj bo za toliko daljša, kot je absolutna vrednost razlike med dolžino originalnega filma in povprečjem dolžin teh (pred letom 1950, s certifikatom ...) filmov. Njihova ocena naj bo za ena nižja od ocene originalnega filma. Kaj bi storili z id?

### Spreminjanje podatkov
Vsem filmom določenega leta, ki imajo oceno nižjo od povprečja filmov v tem letu, dodaj dvakratno razliko med povprečjem in prvotno razliko. Tako bo film z id 22100 namesto ocene 8.4 imel oceno 8.6, saj je prvotno poprečje filmov iz leta 1931 8.5.

### Brisanje podatkov
Delamo z originalno bazo filmi (ena tabela). Želimo pripraviti prikaz aktivnosti določenih režiserjev. Zato bomo zbrisali vse filme tistih režiserjev, ki so režirali več kot 15 filmov (mimogrede so trije, s skupaj 58 filmi!) in jih nadomestili z novim filmom. Ta bo imel naslov Mesanica_, leto nastanka naj bo 2022, opis ustrezen, ocena naj bo povprečje ocen filmov tega režiserja posnetih v prvih in zadnjih dveh letih njegovega ustvarjanja, dolžina pa 10 minut za vsak prvotni film. Ostale podatke si izmisli.

