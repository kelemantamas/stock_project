alphavantage.py
az Alphavantage ingyenes API-járól tölti le a tozsde adatokat 14:00 - 22:00 óra között (francia ido szerint), 
mert us/eastern idozónában az 8:00-16:00
-percenként 5 lekérdezés ingyenes, ezért minden szimbólum lekérdezése után 15 másodpercet várakozik a program,
hogy férjen bele az idokeretbe
naponta 500 lekérdezés ingyenes, ezért 14 és 22 óra között ~11 lekérdezést fog végrehajtani szimbólumonként (40 percenként),
így belefér az 500-as keretbe

pyhton2.7-ben írtam
PyCharm környezetben teszteltem, Conda disztribúciót használtam
adatbázis: MySql, a szerver elindításához XAMPP

config.py tartalma: szimbolumok listája, ezt lehet bovíteni, de nem ajánlatos, mert nem biztos hogy alphavantage-en 
megvan az adott szimbolum API-ja
db - adatbázis 
itt állítsa be az ön adatbázisának a tuljdonságait: host, user, password, dbname
hozzon létre egy új adatbázist, ez lesz a dbname, a többit a program intézi
az adatok egy 'data' nevu táblába töltodnek