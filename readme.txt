alphavantage.py
az Alphavantage ingyenes API-j�r�l t�lti le a tozsde adatokat 14:00 - 22:00 �ra k�z�tt (francia ido szerint), 
mert us/eastern idoz�n�ban az 8:00-16:00
-percenk�nt 5 lek�rdez�s ingyenes, ez�rt minden szimb�lum lek�rdez�se ut�n 15 m�sodpercet v�rakozik a program,
hogy f�rjen bele az idokeretbe
naponta 500 lek�rdez�s ingyenes, ez�rt 14 �s 22 �ra k�z�tt ~11 lek�rdez�st fog v�grehajtani szimb�lumonk�nt (40 percenk�nt),
�gy belef�r az 500-as keretbe

pyhton2.7-ben �rtam
PyCharm k�rnyezetben teszteltem, Conda disztrib�ci�t haszn�ltam
adatb�zis: MySql, a szerver elind�t�s�hoz XAMPP

config.py tartalma: szimbolumok list�ja, ezt lehet bov�teni, de nem aj�nlatos, mert nem biztos hogy alphavantage-en 
megvan az adott szimbolum API-ja
db - adatb�zis 
itt �ll�tsa be az �n adatb�zis�nak a tuljdons�gait: host, user, password, dbname
hozzon l�tre egy �j adatb�zist, ez lesz a dbname, a t�bbit a program int�zi
az adatok egy 'data' nevu t�bl�ba t�ltodnek