import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host='localhost',
                                    user='root',  # change the user and password as needed
                                    password='1394',
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor,
                                    autocommit=True)
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query, data)
                executable = cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # if the query is an insert, return the id of the last row, since that is the row we just added
                    #=====================================================================================
                    # INSERT queries will return the data from the database as a LIST OF DICTIONARIES
                    #=====================================================================================
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    #=====================================================================================
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    #=====================================================================================
                    # if the query is a select, return everything that is fetched from the database
                    # the result will be a list of dictionaries
                    result = cursor.fetchall()
                    return result
                else:
                    #=====================================================================================
                    # UPDATE and DELETE queries will return nothing
                    #=====================================================================================
                    # if the query is not an insert or a select, such as an update or delete, commit the changes
                    # return nothing
                    self.connection.commit()
            # except Exception as e:
            #     # in case the query fails
            #     print("Something went wrong", e)
            #     return False
            finally:
                # close the connection
                self.connection.close()
# this connectToMySQL function creates an instance of MySQLConnection, which will be used by server.py
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection


def connectToMySQL(db):
    return MySQLConnection(db)
