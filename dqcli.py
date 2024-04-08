# dqcli
# usage: python dqcli.py <target> <query>

from dq import *
import sys

target = sys.argv[1]
inquery = ""
for s in sys.argv[2:]:
    inquery += s
    inquery += " " # todo don't put to end
    # print("input query: " + inquery)
d = dq(target)
print(d.q(inquery))
