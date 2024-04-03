
import re
import sys
from tbl import *


specificselect = []
joins = []



# topostfix puts the operators after their operands
def topostfix(query):
  a = re.split(r"([.<])", query) # use parethesis () to keep the delimiter
  a = a[1:] # assume query starts with operator, then first word is '', drop it
  # out = a[0]
  out = ""
  i = 0
  while i < len(a):
    out += a[i+1] + " " + a[i] + " " # a[i]: operator a[i+1]: name
    i += 2
  return out


# findfk finds foreign key from table a to table b
# if more than one, error
def findfk(a, b):
  out = None
  for k in fkfromt[a]:
    if k.tt == b:
      if out != None: # there is already a fk
        print("error: more than one fk from a to b")
        return None
      out = k
  return out


def joinforw(fk):
  return "join " + fk.tt + " on " + fk.ft + "." + fk.fc + " = " + fk.tt + "." + fk.tc

def joinbackw(fk):
  return "join " + fk.ft + " on " + fk.tt + "." + fk.tc + " = " + fk.ft + "." + fk.fc


def join(table, query):
  global joins
  #print(f"query: {query}")
  #print(f"table: {table}")
  query = topostfix(query)
  #print(f"topostfix query: '{query}'")
  words = query.split(" ")
  i = 1
  # for i = 1; i < len(words); i += 2:
  while i < len(words):
    w = words[i]
    if w == "." or w == "<":
      name = words[i-1]
    if w == ".":
      if i >= 0 and words[i-2] == "<": 
        #print("backwards ende starting")
        #print(f"names: {names}")
        tableb = names[len(names)-1]
        joinb = []
        j = len(names)-2
        #for i = len(names) -2; i >=0; i--:
        while j >= 0:
          fk = fkfromtc[tableb][names[j]]
          joinb.append(joinbackw(fk))
          tableb = fk.tt
          j -= 1
        #print(f"tableb: {tableb}, table: {table}")
        if tableb != table:
          fk = findfk(tableb, table)
          #print(f"fk: {fk}")
          joinb.append(joinbackw(fk))
        #print(f"joinb: {joinb}")
        joinb.reverse()
        # append elements from joinb to join
        joins = joins + joinb
        table = names[len(names)-1]
  

      if name in fkfromtc[table]:
        fk = fkfromtc[table][name][0]
        #print(fk)
        joins.append(joinforw(fk))
        table = fk.tt
      else:
        specificselect.append((table, name))


    if w == "<":
      if i <= 1 or words[i-2] == ".": # todo index check
        names = []


      names.append(name)


    if i == len(words)-1:
      #print("backwards ende starting")
      #print(f"names: {names}")
      tableb = names[len(names)-1]
      joinb = []
      j = len(names)-2
      #for i = len(names) -2; i >=0; i--:
      while j >= 0:
        fk = fkfromtc[tableb][names[j]]
        joinb.append(joinbackw(fk))
        tableb = fk.tt
        j -= 1
      #print(f"tableb: {tableb}, table: {table}")
      if tableb != table:
        fk = findfk(tableb, table)
        #print(f"fk: {fk}")
        joinb.append(joinbackw(fk))
      #print(f"joinb: {joinb}")
      joinb.reverse()
      # append elements from joinb to join
      joins = joins + joinb
      table = names[len(names)-1]




    i += 2
  return table




# maketree makes a tree from query
def maketree(query):
  read = ""
  reads = []
  bracketsin = 0
  i = 0;
  while i < len(query):
    c = query[i]
    if c == "(":
      bracketsin += 1
    elif c == ")":
      bracketsin -= 1
    if (c == "(" and bracketsin == 1) or (c == "," and bracketsin == 1) or (c == ")" and bracketsin == 0):
      #print(f"append read: {read}")
      reads.append(read)
      read = ""
      i += 1
      continue
    elif i == len(query) - 1:
      #print(f"append read: {read}")
      read += c # take the last character at string end
      reads.append(read)
    read += c


    i += 1
  #print(f"reads: {reads}")
  out = [reads[0]]
  i = 1
  while i < len(reads):
    out.append(maketree(reads[i]))
    i += 1
  #print(f"out: {out}")
  return out




# run parses queries for node and its children starting from table
def run(table, node):
  t = join(table, node[0])
  for child in node[1:]:
    run(t, child)



configchap = sys.argv[1]
inquery = ""
for s in sys.argv[2:]:
    inquery += s
    inquery += " " # todo don't put to end
# print("input query: " + inquery)
tb = tbl(configchap)
a = re.split(r"; +", inquery) # todo regex?
select = a[0]
#print(f"select: {select}")
where = a[1]
fka = tb.fk()
fkfromtc = tb.fkfromtc(fka)
fkfromt = tb.fkfromt(fka)
#print(fkfromtc)
i = re.search(r"[.<(]", select).start()
selectfrom = select[0:i]
root = maketree(select[i:])
run(selectfrom, root)
# for debugging without () notation
#join(selectfrom, select[i:]) # ".sample.samplelocation.*")
#print(f"joins: {joins}")
joinstring = " \n".join(joins)
selectget = "" # todo change
if len(specificselect) == 0:
  selectget = "*"
else:
  selectget = ", ".join("%s.%s" % tup for tup in specificselect)
gensql = f"select {selectget} from {selectfrom} \n{joinstring} \nwhere {where}"
print(gensql)
db = dbcq(configchap)
# print("generated query: " + sqlquery)
print(db.qfad(gensql))
#print(json.dumps())




