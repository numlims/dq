# dq

usage: python dq.py \<db target\> \<query\>

dq gives dot-notation for foreign keys in sql queries.

it supports queries like

> sampleidcont.sample.location; sampleidcont.psn =
'4020189864'

in sql, the same query would be:

> select s.location from sampleidcont sidc <br>
  join sample s on sidb.sample = s.id <br>
  join samplelocation on sample.samplelocation = samplelocation.id <br>
  where sidc.psn = '4020189864'

## setup

enter your database info in db.example.ini and rename db.example.ini to
db.ini.

the code is in dq.ct. to make, say

```
make
```

if you'd rather edit
[.org](https://orgmode.org/manual/Working-with-Source-Code.html) than
[.ct](https://github.com/tnustrings/codetext), you can convert between
org and ct with ct/orgtoct and ct/cttoorg.

## missing

- maybe prefix all returned values with the name/alias of their table?
- allow update?