# tblhelp.py gives helper functions for tbl

class tblhelp:

    # init tblhelp with a dbcq connection
    def __init__(self, db):
        self.db = db

    # withidentity checks that there are no keys in data that are not columns in table, leaves identity columns in
    def withidentity(self, table, data):
        out = {}
        for k in columns(table):
            if k in data:
                out[k] = data[k]
        return out

    # withoutidentity checks that there are no keys in data that are not columns in table, throws identity columns out
    def withoutidentity(self, table, data):
        identities = self.identity_keys(table)
        for ident in identities:
            if ident in data:
                data.pop(ident)
        return self.withidentity(table, data) # identities is out

    # wherestring returns the keys and values in args as a sql where condition string
    # and appends the values to the args array
    def wherestring(self, dict, args):
        out = ""
        keys = list(dict)
        for i in range(0, len(keys)):
            # build sql query
            # if value None, say is NULL
            if dict[keys[i]] == None:
                out += "[" + keys[i] + "] is null"
            else:
                out += "[" + keys[i] + "] = ? "
            # no comma after last pair
            out += " AND " if i < len(keys)-1 else ""  
            # the args, if None, append nothing
            if dict[keys[i]] != None:
                args.append(dict[keys[i]])
        return out

    # primary_keys queries the primary keys for table and returns them
    # query from https://stackoverflow.com/a/10966944
    # needed?
    def primary_keys(self, table): 
        result = self.db.qfad("""
                  select column_name from information_schema.key_column_usage 
                  where table_name = ? 
                  and constraint_name like 'PK%'""", table)
        out = []
        for row in result:
            out.append(row["column_name"])
        return out

    # primary_keys returns all primary keys as table-indexed dict
    def primary_keys(self):
        result = self.db.qfad("""
                  select table_name, column_name from information_schema.key_column_usage 
                  where constraint_name like 'PK%'""")
        out = {}
        for row in result:
            if not row["table_name"] in out:
                out[row["table_name"]] = []
                out[row["table_name"]].append(row["column_name"])
        return out

    # identity_keys returns the identity columns of table as array
    def identity_keys(self, table):
        result = query_fetch_all_dict(
        """
        select column_name from information_schema.columns
	where columnproperty(object_id(table_schema + '.' + table_name), column_name, 'IsIdentity') = 1
	and table_name = ?""", table)
        out = []
        for row in result:
            out.append(row["column_name"])
        return out

    # columns returns the column names of table as an array of strings,
    # if no table given, return dict by table with columns for every table 
    def columns(self, table=None):
        # return for all tables with columns
        if table==None:
            result = self.db.qfad("""
            select table_name, column_name from information_schema.columns 
            order by ordinal_position""")
            tables = self.tables()
            out = {}
            # make an entry for every table in the dict, even if it doesn't have a column
            for table in tables:
                out[table] = []
            for row in result:
                t = row["table_name"]
                c = row["column_name"]
                if t not in tables: # e.g. schema_version is in result but not in tables
                    continue
                out[t].append(c)
            return out
        
        else: # return columns for specific table
            result = self.db.qfad("""
        select column_name from information_schema.columns 
        where table_name = ? order by ordinal_position""", table)
            out = []
            for row in result:
                out.append(row["column_name"])
            return out

    # columntypes returns a dict of columnnames and types for table
    def columntypes(self, table):
        # query from https://www.mytecbits.com/microsoft/sql-server/list-of-column-names
        query = """
        SELECT
        COLUMN_NAME as name, DATA_TYPE as type
        FROM
        INFORMATION_SCHEMA.COLUMNS
        WHERE
        TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """   
        result = self.db.qfad(query, table) 
        out = {}
        for row in result:
            out[row["name"]] = row["type"]
        return out


    # columns returns the columns for each table
    def columnst(self):
        return self.th.columnst()

    # tables gives the names of the tables in the db
    def tables(self):
        result = self.db.qfad("exec sp_tables")
        tables = []
        for row in result:
            if row["table_owner"] == "dbo":
                tables.append(row["table_name"])
        return tables
