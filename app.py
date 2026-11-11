from flask import Flask
from dotenv import load_dotenv
from routes.user_master_routes import user_master_routes
from routes.appointment_routes import appointment_routes
from routes.provider_routes import provider_routes

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

app.register_blueprint(user_master_routes)
app.register_blueprint(appointment_routes)
app.register_blueprint(provider_routes)

if __name__ == "__main__":
    app.run(debug=True)