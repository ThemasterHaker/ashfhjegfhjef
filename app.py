from modules.database import render_messages, chat_log, log_message, clear_chat, \
    user_signup, \
    check_login, get_user, log_post, get_posts, delete_post, get_recent_posts, get_post
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/", methods=["GET", "POST"])
def index():
    chat_messages = render_messages()
    username = None
    if 'user_id' in session:
        username = get_user(session['user_id'])
    return render_template("index.html", chat_messages=chat_messages, username=username)


@app.route('/clear-chat', methods=['POST'])
def clear_chat_route():
    clear_chat()
    return redirect(url_for('index'))


@app.route("/chat-log", methods=["GET", "POST"])
def get_chat_log():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('usermsg')
        log_message(username, message)
    chat_messages = chat_log()
    return jsonify(chat_messages)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm")
        if user_signup(email, name, password, confirm_password):
            return redirect(url_for("login"))
        else:
            flash("passwords do not match.")
            return redirect(url_for("signup"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user_id, user_email, admin_status = check_login(email, password)

        if user_id is not None:
            session['user_id'] = user_id
            session['user_email'] = user_email
            session['admin'] = admin_status

            return redirect(url_for("index"))
        else:
            return "<h3>invalid login</h3>"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/forum")
def forum():
    if session['user_id']:
        username = get_user(session['user_id'])
        posts = get_posts()
        latest_posts = get_recent_posts()
        return render_template("forum.html", username=username, posts=posts, latest_posts=latest_posts)
    else:
        return redirect(url_for("login"))


@app.route("/create-post", methods=["POST"])
def create():
    username, title, content = "", "", ""
    valid_post = False
    if 'user_id' in session:
        username = get_user(session['user_id'])
        title = request.form.get("title")
        content = request.form.get("post-content")
        valid_post = True
    if valid_post:
        data = {
            'username': username,
            'title': title,
            'content': content
        }
        log_post(data)
        return redirect(url_for("forum"))


@app.route("/delete-post", methods=["POST"])
def delete_post_action():
    if session['admin']:
        post_id = request.form.get("post-id")
        delete_post(post_id)
        return redirect(url_for("forum"))


@app.route("/post/<post_id>")
def view_post(post_id):
    post = get_post(post_id)
    latest_posts = get_recent_posts()
    return render_template("post.html", post=post, latest_posts=latest_posts)


if __name__ == '__main__':
    app.run(debug=True)
