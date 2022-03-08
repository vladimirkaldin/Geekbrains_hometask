6. скрипты характерных выборок (включающие группировки, JOINы, вложенные таблицы);


6.1. Список альбомов, вышедших в 2018 году.

select id, name from albums a2 where released_date = 2018;

6.2. Отсортировать альбомы 2018 года по популярности.

SELECT albums.name, artist.name, COUNT(*) AS total_likes FROM likes 
	join albums
	on likes.target_id = albums.id
	join artist
	on albums.artist_id = artist.id
	where target_type_id = 1 and albums.released_date = 2000
GROUP BY target_id ORDER BY total_likes;


6.3. Показать 10 самых популярных исполнителей.

SELECT artist.name, COUNT(*) AS total_likes FROM likes 
	join artist
	on likes.target_id = artist.id
	where target_type_id = 2
GROUP BY target_id ORDER BY total_likes DESC LIMIT 10;

6.4. Показать 10 самых популярных треков с указанием альбома и исполнителя. 

SELECT track.name as Track_Name, artist.name as Artist_name, albums.name as Album_name, COUNT(*) AS total_likes FROM likes 
	join track
	on likes.target_id = track.id
	join artist
	on track.artist_id = artist.id
	join albums
	on track.album_id = albums.id
	where target_type_id = 5
GROUP BY target_id ORDER BY total_likes DESC LIMIT 10;

==============================================================

7. представления (минимум 2);

7.1. Вывести все альбомы одного исполнителя (id 99)

create or replace view artist_albums as
	select distinct artist.name as Artist, albums.name as Album, albums.released_date as release_date
	from albums, artist
	where albums.artist_id = artist.id and artist.id = 99
order by albums.released_date;


select * from artist_albums;

7.2. Вывести все альбомы жанра 'Поп' за 1990 год

create or replace view pop_albums as
	select distinct artist.name as Artist, albums.name as Album, albums.released_date as release_date
	from albums, artist, genres
	where genre_id = genres.id and genre_id = 4 and albums.artist_id = artist.id and albums.released_date = 1990
order by artist.name;

select * from pop_albums;

===================================================

8. хранимые процедуры / триггеры;

8.1. Процедура возвращает первого любимого артиста пользователя

DELIMITER //
create procedure albums_decade(decade INT(4))
begin 
	case decade
		when '1970' then
		select artist_id, name, released_date from albums a2 where released_date between 1970 and 1979 order by released_date;
		when '1980' then
		select artist_id, name, released_date from albums a2 where released_date between 1980 and 1989 order by released_date;
		when '1990' then
		select artist_id, name, released_date from albums a2 where released_date between 1990 and 1999 order by released_date;
		when '2000' then
		select artist_id, name, released_date from albums a2 where released_date between 2000 and 2009 order by released_date;
		when '2010' then
		select artist_id, name, released_date from albums a2 where released_date between 2010 and 2019 order by released_date;
		when '2020' then
		select artist_id, name, released_date from albums a2 where released_date between 2020 and 2029 order by released_date;
	end case;
end;//

call albums_decade(2000);

8.2. При создании новой записи о песне в track по умолчанию ставит номер id последнего альбома в базе для данного исполнителя. 
Если пользователь вносит другой номер, то отражается внесенный id. 

DELIMITER //
CREATE TRIGGER check_album_id_insert BEFORE INSERT ON track
FOR EACH ROW
BEGIN
  DECLARE alb_id INT;
  SELECT id INTO alb_id FROM albums a2 where track.artist_id = albums.artist_id ORDER BY id DESC LIMIT 1 ;
  SET NEW.album_id = COALESCE(NEW.album_id, alb_id);
end;//

8.3. При заполнении данных по новому треку и альбому отсутвие названия нового альбома в таблице albums означает присваивание альбому 
одноименного названия.

DELIMITER //
CREATE TRIGGER check_album_name_insert BEFORE INSERT ON track
FOR EACH ROW
BEGIN
  DECLARE 
 	album TEXT;
  SELECT track.name, albums.name INTO album FROM track t2, albums a2;
  IF albums.name is null THEN
	insert into albums.name select track.name from track;
	end if;
end;//


