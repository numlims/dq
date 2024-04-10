# qpcli
# usage: python qpcli.py <target> <query>

from qp import *
import sys

target = sys.argv[1]
operation = sys.argv[2]

q = qp(target)

if operation == "select":
    path = sys.argv[3]
    print(f"path: {path}")
    where = sys.argv[4]
    print(f"where: {where}")
    print(q.select(path, where))
    