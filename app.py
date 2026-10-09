from flask import Flask
from dotenv import load_dotenv

from routes.available_details_routes import (
    available_details_routes
)

from routes.added_details_routes import (
    added_details_routes
)

from routes.coordinator_routes import (
    coodinator_routes
)


load_dotenv()


app = Flask(__name__)

app.secret_key = "change-this-to-a-random-secret-key"


app.register_blueprint(
    coodinator_routes
)

app.register_blueprint(
    available_details_routes
)

app.register_blueprint(
    added_details_routes
)


if __name__ == "__main__":
    app.run(debug=True)