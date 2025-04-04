from dq import dq
import sys
def main():
  target = sys.argv[1]
  operation = sys.argv[2]

  d = dq(target)

  if operation == "select":
      path = sys.argv[3]
      where = sys.argv[4]
      print(d.select(path, where))
sys.exit(main())
