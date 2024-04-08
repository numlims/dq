# qpcli
# usage: python qpcli.py <target> <query>

from qp import *
import sys

target = sys.argv[1]
inquery = ""
for s in sys.argv[2:]:
    inquery += s
    inquery += " " # todo don't put to end
    # print("input query: " + inquery)
q = qp(target)
print(q.q(inquery))
