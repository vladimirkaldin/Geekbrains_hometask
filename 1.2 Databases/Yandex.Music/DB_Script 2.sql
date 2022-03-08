drop table if exists users;
CREATE table users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,  
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  phone VARCHAR(16) NOT NULL UNIQUE,
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW() ON UPDATE NOW()
);

drop table if exists photo;
CREATE table photo (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY key,
  name text(100)
);

drop table if exists profiles;
CREATE table profiles (
  user_id INT UNSIGNED NOT NULL PRIMARY KEY,
  gender CHAR(1) NOT NULL,
  birthday DATE,
  hometown VARCHAR(100),
  photo_id INT unsigned,
  constraint profiles_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
  constraint profiles_photo_fk FOREIGN KEY (photo_id) REFERENCES photo(id)
);

drop table if exists artist;
create table artist (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) not null,
	description TEXT(1000) not null,
	photo_id INT unsigned,
	constraint artist_photo_fk FOREIGN KEY (photo_id) REFERENCES photo(id)
);

CREATE INDEX artist_name_idx ON artist(name);

drop table if exists genres;
create table genres (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY key,
	name VARCHAR(100) not null
);


INSERT INTO genres VALUES
  (NULL, 'Инди'),
  (NULL, 'Альтернатива'),
  (NULL, 'Рок-н-ролл'),
  (NULL, 'Поп'),
  (NULL, 'Рок'),
  (NULL, 'Метал'),
  (NULL, 'Электроника'),
  (NULL, 'Танцевальная'),
  (NULL, 'Рэп и хип-хоп'),
  (NULL, 'R&B'),
  (NULL, 'Джаз'),
  (NULL, 'Блюз'),
  (NULL, 'Регги'),
  (NULL, 'Ска'),
  (NULL, 'Панк'),
  (NULL, 'Классика'),
  (NULL, 'Эстрада'),
  (NULL, 'Шансон'),
  (NULL, 'Кантри'),
  (NULL, 'Авторская песня'),
  (NULL, 'Легкая музыка'),
  (NULL, 'Саундтреки'),
  (NULL, 'Музыка мира'),
  (NULL, 'Детская');

drop table if exists labels;
create table labels (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) not null,
	photo_id INT unsigned,
	constraint label_photo_fk FOREIGN KEY (photo_id) REFERENCES photo(id)
);

INSERT INTO labels VALUES
  (NULL, 'Universal Music Group', NULL),
  (NULL, 'Sony Music Entertainment', NULL),
  (NULL, 'Warner Music Group', NULL),
  (NULL, 'Interscope Records', NULL),
  (NULL, 'Polydor Records', NULL),
  (NULL, 'Island Records', NULL),
  (NULL, 'Mercury Records', NULL),
  (NULL, 'Universal Motown', NULL),
  (NULL, 'Columbia Records', NULL),
  (NULL, 'RCA Records', NULL),
  (NULL, 'Sony Classical Records', NULL),
  (NULL, 'Ministry of Sound', NULL),
  (NULL, 'The Orchard', NULL),
  (NULL, 'Atlantic Records', NULL),
  (NULL, 'Warner Records', NULL),
  (NULL, 'Parlophone Records', NULL);


drop table if exists albums;
create table albums (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	artist_id INT unsigned NOT NULL,
	name VARCHAR(100) not null,
	released_date YEAR(4) not null,
	genre_id INT UNSIGNED,
	label_id INT unsigned,
	photo_id INT unsigned,
	constraint album_photo_fk FOREIGN KEY (photo_id) REFERENCES photo(id),
	constraint album_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id),
	constraint album_genre_fk FOREIGN KEY (genre_id) REFERENCES genres(id),
	constraint album_label_fk FOREIGN KEY (label_id) REFERENCES labels(id)
);

CREATE INDEX album_name_idx ON albums(name);




drop table if exists track;
create table track (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	artist_id INT unsigned NOT NULL,
	album_id INT unsigned NOT NULL,
	name VARCHAR(100) not null,
	lyrics TEXT(3000),
	constraint track_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id) on delete cascade,
	constraint track_album_fk FOREIGN KEY (album_id) REFERENCES albums(id) on delete cascade
);

CREATE INDEX track_name_idx ON track(name);


drop table if exists videos;
create table videos (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	artist_id INT unsigned NOT NULL,
	name VARCHAR(100) not null,
	constraint video_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(id)
);

drop table if exists playlists;
create table playlists (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT UNSIGNED NOT NULL,
	name VARCHAR(100) not null,
	track_id INT unsigned NOT NULL,
	constraint playlist_user_fk FOREIGN KEY (user_id) REFERENCES users(id) on delete cascade,
    constraint playlist_track_fk FOREIGN KEY (track_id) REFERENCES track(id)
);

DROP TABLE IF EXISTS target_types;
CREATE TABLE target_types (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO target_types (name) VALUES 
  ('artist'),
  ('album'),
  ('track'),
  ('genre'),
  ('label');

DROP TABLE IF EXISTS likes;
CREATE TABLE likes (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNSIGNED NOT NULL,
  target_id INT UNSIGNED NOT NULL,
  target_type_id INT UNSIGNED NOT null,
  constraint likes_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
  constraint likes_target_type_fk FOREIGN KEY (target_type_id) REFERENCES target_types(id)
);

