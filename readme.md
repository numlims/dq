# dq

usage: python dq.py \<db target\> \<query\>

dq gives dot-notation for sql foreign keys in queries.

it supports queries like

sampleidcont.sample.location; sampleidcont.psn =
'4020189864'

in sql, the same query would be:

select s.* from sampleidcont sidc <br>
  join sample s on sidb.sample = s.id <br>
  join samplelocation on sample.samplelocation = samplelocation.id <br>
  where sidc.psn = '4020189864'

## setup

enter your database info in db.example.ini and mv db.example.ini to
db.ini.

the code is in dq.ct. to make, say

```
make
```

if you'd rather edit .org than .ct, you can convert between org and
ct with ct/orgtoct and ct/cttoorg.

## missing

- maybe offer to alias table names like tablename:alias, for when a table appears twice or more in the same query
- would it be wise to prefix all returned values with the name/alias of their table?