import psycopg2

con = psycopg2.connect(
    host="localhost",
    database="ads",
    user="postgres",
    password="postgres"
)

cur = con.cursor()


def migrations():
    cur.execute("CREATE TABLE IF NOT EXISTS ad(user_id integer, ad_text Text, "
                "price INTEGER, hot_price INTEGER, top BOOLEAN)")
