# Tietokannat-ja-web-ohjelmointi-sulkapallokerho
Sovelluksen perusominaisuudet:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  
- Käyttäjä pystyy lisäämään sovellukseen omia ilmoituksia tulevista tapahtumista ja uutisia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään ilmoituksia.

- Käyttäjä näkee sovellukseen lisätyt ilmoitukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät ilmoitukset.

- Käyttäjä pystyy etsimään ilmoituksia hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä ilmoituksia.

- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät ilmoitukset.

- Ilmoituksille on valittavissa useampia luokitteluja. Valittavissa olevat luokittelut tulee määritellä tietokannassa. Käyttäjä voi valita jokaisen luokittelun kohdalla yhden tai useamman vaihtoehdon.

- Sovelluksessa on pääasiallisen ilmoituksen lisäksi kommentteja, jotka täydentää pääasiallista ilmoitusta. Käyttäjä pystyy lisäämään kommentteja omiin ja muiden käyttäjien ilmoituksiin liittyen.

Sovelluksen tekniset vaatimukset:
- Sovellus on toteutettu samaan tapaan kuin kurssin materiaalissa.

- Sovellus on toteutettu Python-kielellä ja Flask-kirjastoa käyttäen.

- Sovellus käyttää SQLite-tietokantaa.

- Kehitystyössä on käytetty Git-versionhallintaa ja GitHub-palvelua.

- Sovelluksen käyttöliittymä muodostuu HTML-sivuista.

- Sovelluksessa ei ole käytetty JavaScript-koodia.

- Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMin kautta).

- Sovellus ei käytä Flaskin lisäksi muita erikseen asennettavia Python-kirjastoja.

- Sovelluksen ulkoasu (HTML/CSS) on toteutettu itse ilman kirjastoja.

Kuinka sovellusta voi testata:
Alustus: 
1. kloonaa sovellus koneelle sopivaan paikkaan.
2. Luo terminaalin kautta sovelluksen juurihakemistoon venv-tiedosto sekä database.db tietokanta seuraavilla komennoilla:
   python3 -m venv venv
   
   sqlite3 database.db < schema.sql

venv:llä voi hallita moduulin flask toimintaa. Sen tärkeimmät komennot ovat:

source venv/bin/activate  (aktivointi)
deactivate                (lopettaa)

Flask-kirjaston voi asentaa terminaalille seuraavalla komennolla: pip install flask (Ihan vain siltä varalta, jos ei nyt ole valmiiksi sitä. Projektissa pitäisi olla myös toimiva kirjasto.)

Sovelluksen voi käynnistää olemalla sovelluksen kansioissa, käynnistämällä venv:n, johon syötetään: flask run. Terminaali käynnistää palvelimen, josta löytyy sovelluksen osoite. Sen voi kopioida selaimeen, jolloin sovelluksen etusivu aukeaa.

Sovelluksen toiminta:

Etusivulla ei näy paljoakaan mitään, koska käyttäjä ei ole kirjautunut sisään. Sivulla on linkki, joka johtaa käyttäjän kirjautumis sivulle. Joudutaan luomaan uudet tunnukset, koska käyttäjä on hetki sitten luonut sivulle uuden tietokannan. Kirjautumissivulla on linkki tunnuksien luontiin, jonka jälkeen käyttäjä voi kirjautua sisään. Kirjautumisen aikana voi ilmestyä virhesivuja, jos käyttäjä on tehnyt jotain väärin, kuten laittanut väärät tunnukset tai salasanan, varaa jo olemassa olevaa tunnusta tai salasanan luomisen räätälöidyt salasat eivät täsmää.

Kun käyttäjä on kirjautunut sovellukseen, hän voi tarkastella uusimpia ilmoituksia. Niistä näkee otsikon, julkaisijan, julkaisuajan sekä ilmoituksen sisällön. Käyttäjä voi siirtyä ilmoitukseen otsikkoa klikkaamalla. Ilmoituksessa käyttäjä voi joko muokata tai poistaa ilmoituksen. (Tulevaisuudessa ilmoituksen alla voi myös käydä keskustelua. Se tulisi valmiiksi lopullisessa versiossa.)

Etusivulle paluu toteutuu ilmoituksen takaisin etusivulle -linkistä. Etusivulla on myös hakuominaisuus. Käyttäjä voi kirjoittaa etsimänsä ilmoituksen, käyttäjän tai julkaisupäivän, jonka perusteella hakukone etsii sopivat ilmoitukset ja esittää ne käyttäjälle. Haku antaa tyhjän sivun, jos sopivaa ilmoitusta ei löydy.

Sivulta voidaan kirjautua ulos etusivulta. Sivu ei kirjaa käyttäjää automaattisesti pois palvelimen suljettua, mutta se tulee korjatuksi tulevaisuudessa tietoturvan tähden. 
