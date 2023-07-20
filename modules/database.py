import psycopg2
from psycopg2 import pool
import bcrypt

db = 'postgres://snow:I7dBCaGnnvOlanqxcbzgk7tPtWvFcOwO@dpg-cip5t4unqql4qa1qcr20-a/cozydb'
# db = 'postgres://snow:I7dBCaGnnvOlanqxcbzgk7tPtWvFcOwO@dpg-cip5t4unqql4qa1qcr20-a.singapore-postgres' \
#      '.render.com/cozydb'

min_conn = 1
max_conn = 10

conn_pool = psycopg2.pool.SimpleConnectionPool(min_conn, max_conn, db)


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
    return result


def chat_log():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT username, message FROM messages ORDER BY id DESC LIMIT 8')
    result = cur.fetchall()
    chat_messages = [{'username': row[0], 'msg': row[1]} for row in result]
    cur.close()
    release_conn(conn)
    return chat_messages


def clear_chat():
    query = 'DELETE FROM messages'
    params = []
    sql_write(query, params)


def user_signup(email, name, password, confirm_password):
    if password == confirm_password:

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        query = "INSERT INTO users (email, name, pw_hash) VALUES (%s, %s, %s)"
        params = (email, name, pw_hash,)

        sql_write(query, params)

        return True
    else:
        return False


def check_login(user_email, user_pw):
    result = sql_select("SELECT id, email, pw_hash, admin FROM users WHERE email = %s", (user_email,))

    if result and bcrypt.checkpw(user_pw.encode(), result[0][2].encode()):
        user_id = result[0][0]
        user_email = result[0][1]
        admin_status = result[0][3]

        return user_id, user_email, admin_status
    else:
        return None


def get_user(user_id):
    query = "SELECT name FROM users WHERE id = %s"
    params = (user_id,)
    result = sql_select(query, params)
    username = result[0][0]
    return username


def log_post(data):
    query = "INSERT INTO posts (username, title, content) VALUES (%s, %s, %s)"
    username, title, content = data['username'], data['title'], data['content']
    params = (username, title, content)
    sql_write(query, params)
    return f"logged a new post from {username}!"


def get_posts():
    query = "SELECT * FROM posts;"
    params = ()
    result = sql_select(query, params)
    return result
