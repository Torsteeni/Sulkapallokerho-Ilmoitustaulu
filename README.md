# Sulkapallokerhon ilmoitustaulu

Sovelluksen ominaisuudet:

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen omia ilmoituksia tulevista sulkapallotapahtumista. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään ilmoituksia.
* Käyttäjä näkee sovellukseen lisätyt ilmoitukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät ilmoitukset.
* Käyttäjä pystyy etsimään ilmoituksia päivänmäärän perusteella. 
* Käyttäjä pystyy ilmoittautumaan eri tapahtumiin.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät ilmoitukset.
* Ilmoituksille on valittavissa useampia luokitteluja. Valittavissa olevat luokittelut tulee määritellä tietokannassa. Käyttäjä voi valita jokaisen luokittelun kohdalla yhden tai useamman vaihtoehdon.
* Sovelluksessa on pääasiallisen ilmoituksen lisäksi tapahtumasta voi käydä keskustelua.





Sovelluksen asentaminen:



1. kopioit sovelluksen koneelle
2. Hae sovellus terminaalista ja suorita: python3 -m venv venv
3. aktivoi venv: source venv/bin/activate
4. Asenna flask kirjasto ja tarvittava tietokanta:

&#x20;   - pip install flask

&#x20;   - sqlite3 database.db < schema.sql

5\. Suorita flask run, jonka jälkeen sovelluksen tulisi toimi osoitteessa http://127.0.0.1:5000

