import psycopg2
import bcrypt


db = "cozydb"


def connect():
    conn = psycopg2.connect(f"dbname={db}")
    cur = conn.cursor()
    return conn, cur


def close(conn, cur):
    cur.close()
    conn.close()


def sql_select(query, params):
    conn, cur = connect()
    cur.execute(query, params)
    result = cur.fetchall()
    close(conn, cur)
    return result


def sql_write(query, params):
    conn, cur = connect()
    cur.execute(query, params)
    conn.commit()
    close(conn, cur)


def log_message(message):
    query = 'INSERT INTO messages (message, username) VALUES (%s, %s)'
    params = (message['msg'], message['username'])
    sql_write(query, params)


def render_messages():
    conn, cur = connect()
    cur.execute('SELECT username, message FROM messages ORDER BY id DESC LIMIT 8')
    result = cur.fetchall()
    close(conn, cur)
    return result
