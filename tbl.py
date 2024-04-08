# tbl.py gives functions for sql table handling and inspection
# see method comments for short description

# columns
# columntypes
# deletefrom
# insert
# fk
# fkfromt
# fkfromtc
# fktot
# (fktotc)
# identities
# pk
# tables

from dbcq import *
from tblhelp import tblhelp

class fk:
    def __init__(self, ft, fc, tt, tc):
        self.ft = ft
        self.fc = fc
        self.tt = tt
        self.tc = tc

class tbl:

    # init connects to the database target in db.ini
    def __init__(self, target):
        self.db = dbcq(target)
        self.th = tblhelp(self.db)

    # columns returns the column names of table as an array of strings,
    # if no table given, return dict by table with columns for every table 
    def columns(self, table=None):
        return self.th.columns(table)

    # columntypes gives the column schema for tablename
    def columntypes(self, tablename):
        return self.th.columntypes(tablename)

    # deletefrom deletes the row in table identified by the post parameters
    # if there are two rows with exactly the same values, it deletes both 
    def deletefrom(self, table, row):
        args = []
        q = "delete from [" + table + "] where " + self.th.wherestring(row, args)
        # do the deleting
        self.db.query(q, args) # todo uncomment

    # identities gives list of identity (auto-increment) columns for table
    def identities(self, table):
        identities = self.th.identity_keys(table)
        return identities

    # insert inserts a line in a table
    def insert(self, table, row):
        data = withoutidentity(table, row) # assume primary key is generated
        types = columntypes(table) # for parsing
        placeholders = [] # for query
        for key in data:
            # parse strings to numbers
            if types[key] in ["int", "bigint", "smallint", "tinyint", "bit", "decimal", "numeric", "money", "smallmoney"]:
                data[key] = int(data[key])
            elif types[key] in ["real", "float"]:
                data[key] = float(data[key])

            # a placeholder for the query
            placeholders.append("?")
    
        q = "insert into [" + table + "] ([" + "], [".join(list(data)) + "]) values (" + ", ".join(placeholders) + ")"

        # do the insertion
        self.db.query(q, *data.values()) 

    # fk gives all foreign keys as array of dicts [{ft, fc, tt, tc}]. ft: from table, fc: from colum, tt: to table, tc: to column.
    def fk(self):
        # query from https://stackoverflow.com/a/17501870
        query = """
        SELECT 
        OBJECT_NAME(fk.parent_object_id) ft,
        COL_NAME(fkc.parent_object_id, fkc.parent_column_id) fc,
        OBJECT_NAME(fk.referenced_object_id) tt,
        COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) tc
        FROM 
        sys.foreign_keys AS fk
        INNER JOIN 
        sys.foreign_key_columns AS fkc 
        ON fk.OBJECT_ID = fkc.constraint_object_id
        INNER JOIN 
        sys.tables t 
        ON t.OBJECT_ID = fkc.referenced_object_id"""

        # return self.db.qfad(query) # todo return array of keys? let key have fields ft fc tt tc and fromtable fromcolumn totable tocolumn?
        rows = self.db.qfad(query) # todo return array of keys? let key have fields ft fc tt tc and fromtable fromcolumn totable tocolumn?
        # output foreign as objects
        a = []
        for row in rows:
            # a.append(fk(row["ft"].lower(), row["fc"].lower(), row["tt"].lower(), row["tc"].lower())) # is lower() here a good idea?
            a.append(fk(row["ft"], row["fc"], row["tt"], row["tc"])) # is lower() here a good idea?
            # a.append(row)
        return a

    # fkfromt returns foreign key array as dict indexed by from-table
    def fkfromt(self, fka):
        fkt = {}
        for key in fka:
            if not key.ft in fkt:
                fkt[key.ft] = []
            fkt[key.ft].append(key)
        return fkt

    # fkfromtc returns foreign key array as dict indexed by from-table and from-column
    def fkfromtc(self, fka):
        fktc = {}
        for key in fka:
            # is there an entry for the table?
            if not key.ft in fktc:
                fktc[key.ft] = {}
            # is there an entry for the key?
            if not key.fc in fktc[key.ft]:
                fktc[key.ft][key.fc] = []
            fktc[key.ft][key.fc].append(key)
        return fktc

    # fktot returns foreign keys by to-table
    def fktot(self, fka):
        out = {}
        for key in fka:
            if not key.tt in out:
                out[key.tt] = []
            out[key.tt].append(key)
        return out

    # fktot returns foreign keys by to-table and to-column
    def fktotc(self, fka):
        out = {}
        for key in fka:
            if not key.tt in out:
                out[key.tt] = {}
            if not key.tc in out[key.tt]:
                out[key.tt][key.tc] = []
            out[key.tt][key.tc].append(key)
        return out

    # also fktotc?

    # pk gives primary keys as list for each table
    def pk(self):
        return self.th.primary_keys()

    # tables gives the names of the tables in the db
    def tables(self):
        return self.th.tables()

    # update updates data in a table row
    def update(self, table, fromrow, torow):
        fromdata = withidentity(table, fromrow)
        todata = withoutidentity(table, torow)

        # todata.pop(pk) # don't update the primary key
        updatepairs = []
        args = [] # successively fill the query args array
        # update pairs
        for key in todata:
            # build sql query
            updatepairs.append("[" + key + "] = ?")
            # the args
            args.append(todata[key])

        ws = self.th.wherestring(fromdata, args) # fill args along the way
        q = "update [" + table + "] set " + ", ".join(updatepairs) + " where " + ws

        # do the update
        self.db.query(q, args)

