from modules.database import sql_select, sql_write, render_messages, log_message, connect, close
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/", methods=["GET", "POST"])
def index():
    chat_messages = render_messages()
    return render_template("index.html", chat_messages=chat_messages)


@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    log_message(data)
    send({'data': data}, event='server_response', broadcast=True)


@app.route('/clear-chat', methods=['POST'])
def clear_chat():
    query = 'DELETE FROM messages'
    sql_write(query, [])

    return redirect(url_for('index'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        pass
    else:
        return render_template("signup.html")


@app.route("/chat-log", methods=["GET"])
def chat_log():
    conn, cur = connect()
    cur.execute('SELECT username, message FROM messages ORDER BY id DESC LIMIT 8')
    result = cur.fetchall()
    chat_messages = [{'username': row[0], 'msg': row[1]} for row in result]
    close(conn, cur)
    return jsonify(chat_messages)


if __name__ == '__main__':
    socketio.run(app, debug=True)
