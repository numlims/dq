# dq

usage: python dq.py \<db target\> \<query\>

dq gives dot-notation for foreign keys in sql queries.

it supports queries like

> select sampleidcont.sample.location; sampleidcont.psn =
'59493038'

in sql, the same query would be:

> select s.location from sampleidcont sidc <br>
  join sample s on sidb.sample = s.id <br>
  join samplelocation on sample.samplelocation = samplelocation.id <br>
  where sidc.psn = '59493038'

backward joins are noted with <. starting from the sample table, the
query above could also be written as

> select sample(<sampleidcont.psn, .location); sampleidcont.psn = '59493038'

the brackets mean that both <sampleidcont.psn and .location are joined
to sample.

## setup

rename db.example.ini to db.ini and enter your database info.

to make, say

```
make
```

the code is in dq.ct. if you'd rather edit
[.org](https://orgmode.org/manual/Working-with-Source-Code.html) than
[.ct](https://github.com/tnustrings/codetext), you can convert between
org and ct with ct/orgtoct and ct/cttoorg.

## missing

- maybe prefix all returned values with the name/alias of their table?
- python api and cli interface
- allow update etc? https://stackoverflow.com/a/1293347

## license

[cc0](https://creativecommons.org/publicdomain/zero/1.0/)