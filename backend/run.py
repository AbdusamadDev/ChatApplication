from flask import Flask
from api import api_blueprint as api
from flask_cors import CORS


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../templates/static",
    static_url_path="/static",
)
CORS(app, origins=["*"], supports_credentials=True)

app.register_blueprint(api)
app.run("0.0.0.0", 5000, debug=True)
