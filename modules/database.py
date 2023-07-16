import psycopg2
from psycopg2 import pool

db = 'postgres://snow:I7dBCaGnnvOlanqxcbzgk7tPtWvFcOwO@dpg-cip5t4unqql4qa1qcr20-a/cozydb'

minconn = 1
maxconn = 10

conn_pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, db)


def get_conn():
    return conn_pool.getconn()


def release_conn(conn):
    conn_pool.putconn(conn)


def sql_select(query, params):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    release_conn(conn)
    return result


def sql_write(query, params):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    release_conn(conn)


def log_message(message):
    query = 'INSERT INTO messages (username, message) VALUES (%s, %s)'
    params = (message['username'], message['msg'])
    sql_write(query, params)


def render_messages():
    query = 'SELECT username, message FROM messages ORDER BY id DESC LIMIT 8'
    return sql_select(query, [])
