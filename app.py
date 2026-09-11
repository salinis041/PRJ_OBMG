from flask import Flask
from dotenv import load_dotenv

from routes.patient_routes import patient_routes


load_dotenv()

app = Flask(__name__)

app.register_blueprint(patient_routes)


if __name__ == "__main__":
    app.run(debug=True)