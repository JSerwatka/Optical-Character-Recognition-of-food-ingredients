import sqlite3 as sql

conn = sql.connect('product_substances.db')

cursor = conn.cursor()

# cursor.execute("""DROP TABLE substances""")
# # create table of substances
# cursor.execute(""" CREATE TABLE IF NOT EXISTS substances(
#                 name_of_substance text,
#                 e_code text,
#                 harmfulness integer
# )""")
#
# # insert into table
# cursor.execute(""" INSERT INTO substances VALUES
#                 ("kwasek cytrynowy", NULL, 3),
#                 ("halo to ja", "test", 3)
# """)
#
cursor.execute(""" SELECT * FROM substances""")
print(cursor.fetchall())

conn.commit()

conn.close()