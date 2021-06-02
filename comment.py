import sqlite3 as sl

def storecom(first,second):
    comlist= [first,second]

    try:

        with con:  # table with all the different columns that will be used, and type of data
            con.execute("""               
                    CREATE TABLE COMMENTS (
                        first_name TEXT,
                        opinion TEXT                       
                        );
                """)
    except:
        print("Table already exists.")
    con = sl.connect('walrus.db')
    sql = 'INSERT INTO COMMENTS (first,second) values(?, ?)'
    with con:
        con.execute(sql, comlist)
    with con:
        data = con.execute("SELECT * FROM COMMENTS")
    for row in data:
        print(row)

    return
