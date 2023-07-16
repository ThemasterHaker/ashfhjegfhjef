from modules.database import sql_write, render_messages, log_message, get_conn, release_conn, chat_log
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")


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
def get_chat_log():
    try:
        chat_messages = chat_log()
        return jsonify(chat_messages)
    except Exception as e:
        print(f"Error in get_chat_log: {e}")  # Add this line
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    socketio.run(app, debug=False)
