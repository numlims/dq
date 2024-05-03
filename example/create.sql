create table album (
  id integer primary key,
  title text,
  year integer
);
create table song (
  id integer primary key,
  title text,
  album integer,
  foreign key (album)
    references album (id)
    on delete cascade
);

