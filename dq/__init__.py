
import jsonpickle
import re
from tbl import *



# both gives name and alias if alias is non null
def both(a, b):
  return a + (" " + b if b != None else "")


# one gives the first, if it is null, the second
def one(a, b):
  if a == None:
    return b
  return a


# splitas returns tuple of tablename and alias
def splitas(s):
  a = s.split(":")
  if len(a) > 2:
    print("error: alias tables with name:alias")
    exit
  if len(a) == 1:
    return (a[0], None)
  return (a[0], a[1])


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


def joinforw(fk, asfrom, asto, lri):
  return lri + " join " + both(fk.tt, asto) + " on " + one(asfrom, fk.ft) + "." + fk.ff + " = " + one(asto, fk.tt) + "." + fk.tf

def joinbackw(fk, asfrom, asto, lri):
  return lri + " join " + both(fk.ft, asfrom) + " on " + one(asto, fk.tt) + "." + fk.tf + " = " + one(asfrom, fk.ft) + "." + fk.ff


# maketree makes a tree from query
def maketree(query):
  read = ""
  reads = []
  bracketsin = 0
  i = 0;
  while i < len(query):
    c = query[i]
    if c == "{":
      bracketsin += 1
    elif c == "}":
      bracketsin -= 1
    if (c == "{" and bracketsin == 1) or (c == "," and bracketsin == 1) or (c == "}" and bracketsin == 0):
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





class dq:
  def test(self):
    # is fkfromt reachable without self
    print("")
    print(specificselect)
    #print(fkfromt)
  

  def __init__(dq, target):
    dq.specificselect = []
    dq.tb = tbl(target)
    dq.db = dbcq(target)
    dq.joins = []
    fka = dq.tb.fk()
    dq.fkfromtf = dq.tb.fkfromtf(fka)
    dq.fkfromt = dq.tb.fkfromt(fka)
    #self.test()
    #print(fkfromt)
  

  

  # findfk finds foreign key from table a to table b
  # if more than one, error
  def findfk(self, a, b):
    out = None
    for k in self.fkfromt[a]:
      if k.tt == b:
        if out != None: # there is already a fk
          print("error: more than one fk from a to b")
          return None
        out = k
    return out
  

  def join(dq, table, tablealias, query):
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
        (name, alias) = splitas(words[i-1])
        lri = ""
        if re.match(r"^\(l\)", name):
          lri = "left"
        elif re.match(r"^\(r\)", name): 
          lri = "right"
        elif re.match(r"^\(i\)", name):
          lri = "inner"
        # delete the lri tag from name
        name = re.sub(r"^\(.\)", "", name)
  

      if w == ".":
        if i >= 0 and words[i-2] == "<": 
          #print("backwards ende starting")
          #print(f"names: {names}")
          tableb = names[len(names)-1]
          aliasb = aliases[len(names)-1]
          joinb = []
          j = len(names)-2
          while j >= 0:
            fk = dq.fkfromtf[tableb][names[j]]
            joinb.append(joinbackw(fk, aliasb, aliases[j], lris[j]))
            tableb = fk.tt
            aliasb = aliases[j]
            j -= 1
          #print(f"tableb: {tableb}, table: {table}")
          if tableb != table:
            fk = dq.findfk(tableb, table)
            #print(f"fk: {fk}")
            joinb.append(joinbackw(fk, aliasb, None, lris[len(names)-1])) # todo is None as lri right?
          #print(f"joinb: {joinb}")
          joinb.reverse()
          # append elements from joinb to join
          dq.joins = dq.joins + joinb
          table = names[len(names)-1]
          tablealias = aliases[len(names)-1]
    

        if name in dq.fkfromtf[table]:
          fk = dq.fkfromtf[table][name][0]
          #print(fk)
          dq.joins.append(joinforw(fk, tablealias, alias, lri))
          table = fk.tt
          tablealias = alias
        else:
          dq.specificselect.append((table, tablealias, name))
  

      if w == "<":
        if i <= 1 or words[i-2] == ".": # todo index check
          names = []
          aliases = []
          lris = []
  

        names.append(name)
        aliases.append(alias)
        lris.append(lri)
  

      if i == len(words)-1:
        #print("backwards ende starting")
        #print(f"names: {names}")
        tableb = names[len(names)-1]
        aliasb = aliases[len(names)-1]
        joinb = []
        j = len(names)-2
        while j >= 0:
          fk = dq.fkfromtf[tableb][names[j]]
          joinb.append(joinbackw(fk, aliasb, aliases[j], lris[j]))
          tableb = fk.tt
          aliasb = aliases[j]
          j -= 1
        #print(f"tableb: {tableb}, table: {table}")
        if tableb != table:
          fk = dq.findfk(tableb, table)
          #print(f"fk: {fk}")
          joinb.append(joinbackw(fk, aliasb, None, lris[len(names)-1])) # todo is None as lri right?
        #print(f"joinb: {joinb}")
        joinb.reverse()
        # append elements from joinb to join
        dq.joins = dq.joins + joinb
        table = names[len(names)-1]
        tablealias = aliases[len(names)-1]
  

  

      i += 2
    return (table, tablealias)
  

  

  # run parses queries for node and its children starting from table
  def run(dq, table, alias, node):
    (t, a) = dq.join(table, alias, node[0])
    for child in node[1:]:
      dq.run(t, a, child)


  # selectwild gives selectionstring for wildcard select
  def selectwild(self, table, alias):
    gets = []
    for c in self.tb.fields()[table]: # fields()[table]: quick fix 
      s = "%s.%s" % (one(alias, table), c)
      gets.append(f"{s} as '{s}'")
    return ", ".join(gets)


  # select handles queries to dq
  def select(dq, select, where):
    select = select.lower() # is lowering ok here?
    #print(f"select: {select}")
    i = re.search(r"[.<{]", select).start()
    (selectfrom, selectfromalias) = splitas(select[0:i])
    root = maketree(select[i:])
    dq.run(selectfrom, selectfromalias, root)
    # for debugging without {} notation
    #join(selectfrom, select[i:]) # ".sample.samplelocation.*")
    #print(f"joins: {joins}")
    joinstring = " \n".join(dq.joins)
    selectget = "" # todo change
    if len(dq.specificselect) == 0:
      # selectget = "*"
      selectget = dq.selectwild(selectfrom, selectfromalias)
    else:
      #print(f"specificselect: {specificselect}")
      gets = []
      for tri in dq.specificselect:
        table = tri[0]
        alias = tri[1]
        col = tri[2]
  
        # if col is wildcard, name each column explicitly
        if col == "*":
          gets.append(dq.selectwild(table, alias))
        else: # explicit named columns
          s = "%s.%s" % (one(alias, table), col)
          gets.append(f"{s} as '{s}'")
      selectget = ", ".join(gets)
      #selectget = ", ".join("%s.%s" % (one(trip[1], trip[0]), trip[2]) for trip in specificselect)
    gensql = f"select {selectget} from {both(selectfrom, selectfromalias)} \n{joinstring} \nwhere {where}"
    print(gensql)
    # print("generated query: " + sqlquery)
    return dq.db.qfad(gensql)
    #print(json.dumps())
  






