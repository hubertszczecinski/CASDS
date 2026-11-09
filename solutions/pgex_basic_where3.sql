-- CASDS | zadanie: pgex_basic_where3 | trudność: easy
--
-- # Basic string searches
--
-- How can you produce a list of all facilities with the word 'Tennis' in their name?
--
-- ## Schemat bazy
--
-- cd.bookings (bookid INTEGER, facid INTEGER, memid INTEGER, starttime timestamp, slots
-- INTEGER)
-- cd.facilities (facid INTEGER, name varchar, membercost numeric, guestcost numeric,
-- initialoutlay numeric, monthlymaintenance numeric)
-- cd.members (memid INTEGER, surname varchar, firstname varchar, address varchar, zipcode
-- INTEGER, telephone varchar, recommendedby INTEGER, joindate timestamp)
-- Klucze główne: bookings(bookid), facilities(facid), members(memid). Klucze obce:
-- bookings.facid → facilities.facid, bookings.memid → members.memid, members.recommendedby
-- → members.memid.
--
--
-- ## Oczekiwany wynik
--
-- Wartości kolumn oddzielone znakiem | (3 wierszy). Kolejność wierszy nie ma znaczenia.
--
-- 0|Tennis Court 1|5|25|10000|200
-- 1|Tennis Court 2|5|25|8000|200
-- 3|Table Tennis|0|5|320|10
--
-- Napisz zapytanie SQL (dialekt SQLite). Baza `cd` jest podpięta tylko do odczytu, a wynik
-- porównujemy z wzorcowym: liczą się wartości i kolejność kolumn, nazwy kolumn nie.
-- Polecenia zaczynające się od kropki (np. .headers) są niedozwolone.

-- TODO: Twoje zapytanie
SELECT *
FROM cd.facilities
WHERE name LIKE '%Tennis%';