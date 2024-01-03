from api import api_blueprint as api
from flask_cors import CORS
from flask import Flask

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../templates/static",
    static_url_path="/static",
)
CORS(app, origins=["*"], supports_credentials=True)


if __name__ == "__main__":
    app.register_blueprint(api)
    app.run("0.0.0.0", 5000, debug=True)
