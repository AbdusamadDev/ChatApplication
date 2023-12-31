from flask import Blueprint, render_template

api_blueprint = Blueprint("API for serving templates", __name__)


@api_blueprint.route("/chat", methods=["GET"])
def chat_handler():
    return render_template("chat.html")


@api_blueprint.route("/design", methods=["GET"])
def design_handler():
    return render_template("designed_chat.html")
