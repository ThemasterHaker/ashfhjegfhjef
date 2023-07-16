import psycopg2
from flask import render_template
from psycopg2 import pool

db = 'postgres://snow:I7dBCaGnnvOlanqxcbzgk7tPtWvFcOwO@dpg-cip5t4unqql4qa1qcr20-a/cozydb'
# db = "cozydb"


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


def log_message(username, message):
    query = 'INSERT INTO messages (username, message) VALUES (%s, %s)'
    params = (username, message)
    sql_write(query, params)


def render_messages():
    query = 'SELECT username, message FROM messages ORDER BY id DESC LIMIT 8'
    result = sql_select(query, ())
    return render_template("index.html", chat_messages=result)


def chat_log():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT username, message FROM messages ORDER BY id DESC LIMIT 8')
        result = cur.fetchall()
        chat_messages = [{'username': row[0], 'msg': row[1]} for row in result]
        cur.close()
        release_conn(conn)
        return chat_messages
    except Exception as e:
        print(f"Error in chat_log: {e}")

