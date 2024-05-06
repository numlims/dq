# dq

usage: python dq.py \<db target\> select \<query\> \<where\>

dq gives dot notation for sql queries.

it supports queries like

> select("sampleidcont.sample.location", "sampleidcont.psn =
'59493038'")

in sql, the same query would be:

> select s.location from sampleidcont sidc <br>
  join sample s on sidc.sample = s.id <br>
  join samplelocation on sample.location = samplelocation.id <br>
  where sidc.psn = '59493038'

forward joins (left to right) are noted with ".". backward joins
(right to left) are noted with "<". starting from the sample table,
the query above could also be written as

> select("sample{<sampleidcont.psn, .location}", "sampleidcont.psn = '59493038'")

the brackets {} mean that both '<sampleidcont.psn' and '.location'
hang on sample.

## setup

rename db.example.ini to db.ini and enter your database info.

rename dbc.example.ini to dbc.ini and link to your db.ini from
it. there are two ini files so that you can put db.ini with sensitive
connection info in another directory.

to make, say

```
make
```

the code is in dq.ct. if you'd rather edit
[.org](https://orgmode.org/manual/Working-with-Source-Code.html) than
[.ct](https://github.com/tnustrings/codetext), you can convert between
org and ct with ct/orgtoct and ct/cttoorg.

## sqlite example

create a little sqlite example db with example/musicdb.ct.

cd into example, make and run it:

```
cd example
make
sh musicdb.sh
```

put music.db in the your db.ini like this:

```
[music]
type = sqlite
database = /path/to/music.db
```

then, back in the dq directory, you can say

```
python dq.py music select "song.album.title", "song.title='rocks off'"
```

or, using backward (<) notation:

```
python dq.py music select "album{<song.*, .title}", "song.title='rocks off'"
```

## missing

- maybe a prefixstrip option to query and output without prefix common to tablenames.
- maybe update etc? https://stackoverflow.com/a/1293347 for now you can update, insert and delete via tbl

## license

[cc0](https://creativecommons.org/publicdomain/zero/1.0/)