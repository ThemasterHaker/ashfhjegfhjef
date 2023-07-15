import psycopg2

db = 'postgres://snow:I7dBCaGnnvOlanqxcbzgk7tPtWvFcOwO@dpg-cip5t4unqql4qa1qcr20-a/cozydb'


def connect():
    conn = psycopg2.connect(db)
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
    query = 'INSERT INTO messages (username, message) VALUES (%s, %s)'
    params = (message['username'], message['msg'])
    sql_write(query, params)


def render_messages():
    conn, cur = connect()
    cur.execute('SELECT username, message FROM messages ORDER BY id DESC LIMIT 8')
    result = cur.fetchall()
    close(conn, cur)
    return result
