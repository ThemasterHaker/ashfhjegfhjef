from modules.database import sql_write, render_messages, chat_log, log_message
from flask import Flask, render_template, request, redirect, url_for, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route("/", methods=["GET", "POST"])
def index():
    chat_messages = render_messages()
    return render_template("index.html", chat_messages=chat_messages)


@app.route('/clear-chat', methods=['POST'])
def clear_chat():
    query = 'DELETE FROM messages'
    sql_write(query, [])
    return redirect(url_for('index'))


@app.route("/chat-log", methods=["GET", "POST"])
def get_chat_log():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('usermsg')
        log_message(username, message)
    chat_messages = chat_log()
    return jsonify(chat_messages)


if __name__ == '__main__':
    app.run(debug=True)
