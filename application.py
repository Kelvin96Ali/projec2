from flask import Flask, render_template, redirect, request, flash, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import os
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

active_user_list = ["momo"]
active_chatrooms = {
    "rooms": [
        {
            "name": "TestRoom1",
            "disc": "First Test room",
            "messages": [
                {"author": "AdminUser", "body": "AdminMessage", "time_stamp": "now"},
            ],
        }
    ]
}

# Funciones auxiliares
def find_room(room_name):
    for index, room in enumerate(active_chatrooms["rooms"]):
        if room_name in room["name"]:
            return index
    return None

def check_for_message_limit(room_name):
    index = find_room(room_name)
    if len(active_chatrooms["rooms"][index]["messages"]) > 99:
        active_chatrooms["rooms"][index]["messages"].pop(0)
        check_for_message_limit(room_name)

# Rutas
@app.route("/")
def index():
    if "username" not in session:
        session["username"] = None
    if "current_room" not in session:
        session["current_room"] = None

    if session["username"] is not None:
        if session["current_room"] is None:
            return redirect(url_for("chat_selection"))
        return redirect(url_for("display_chat", room_name=session["current_room"]))
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_to_register = request.form.get("username")
        if user_to_register in active_user_list:
            flash("Sorry, nickname already taken!")
            return redirect(url_for("login"))
        else:
            active_user_list.append(user_to_register)
            session["username"] = user_to_register
            return redirect(url_for("chat_selection"))
    return render_template("landing_page.html")

@app.route("/logout", methods=["GET"])
def logout():
    if session["username"] in active_user_list:
        active_user_list.remove(session["username"])
    session["username"] = None

    return redirect(url_for("login"))

@app.route("/select_chat", methods=["POST", "GET"])
def chat_selection():
    if "current_room" not in session:
        session["current_room"] = None
    if session["current_room"] is not None:
        session["current_room"] = None
    if request.method == "POST":
        new_chatroom_name = request.form.get("newChatName")
        new_chatroom_disc = request.form.get("newChatDisc")
        if find_room(new_chatroom_name) is None:
            active_chatrooms["rooms"].append(
                {"name": new_chatroom_name, "disc": new_chatroom_disc, "messages": []}
            )
            return redirect(url_for("display_chat", room_name=new_chatroom_name))
        else:
            flash("Room name already taken!")

    return render_template("chat_selection_page.html", rooms=active_chatrooms["rooms"])

@app.route("/room/<string:room_name>", methods=["POST", "GET"])
def display_chat(room_name):
    try:
        for room in active_chatrooms["rooms"]:
            if room_name in room["name"]:
                session["current_room"] = room_name
                return render_template(
                    "chatroom.html", room=room, user=session["username"]
                )
        raise KeyError("Room was not found in active_chatrooms")
    except KeyError as err:
        print(err)
        flash("Room was not found. Please choose one of available rooms")
        return redirect(url_for("chat_selection"))

@app.route("/room/api/messages/<string:room_name>", methods=["GET"])
def get_messages(room_name):
    index = find_room(room_name)
    messages = active_chatrooms["rooms"][index]["messages"]
    return jsonify(messages)

@socketio.on("submit message")
def insert_message(message):
    room_name = session["current_room"]
    author = session["username"]
    time_stamp = datetime.datetime.now().isoformat(timespec="minutes").split("T")
    check_for_message_limit(room_name)
    new_message = {
        "author": author,
        "body": message["message"],
        "time_stamp": f"{time_stamp[0]} {time_stamp[1]}",
    }
    index = find_room(room_name)
    active_chatrooms["rooms"][index]["messages"].append(new_message)
    emit("add messages", new_message, broadcast=True)

if __name__ == "__main__":
    app.debug = True
    app.env = "development"
    socketio.run(app)
