import json
from pathlib import Path

from flask import Flask, request, jsonify, g
from pydantic import ValidationError
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import ClinicalData
from schemas import ClinicalDataCreate

app = Flask(__name__)

# Create the SQLite database table if it does not exist
Base.metadata.create_all(bind=engine)

# Set up JSON Lines storage
DATA_FILE = Path("data/clinical_data.jsonl")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def append_to_file(record):
    """Append a clinical record to the JSON Lines file."""
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


# Open a database session for each request
@app.before_request
def create_session():
    g.db = SessionLocal()


# Close the database session after each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    db = getattr(g, "db", None)

    if db is not None:
        db.close()


# POST: Create a clinical record
@app.route("/clinical/", methods=["POST"])
def create_record():
    try:
        payload = request.get_json()
        if not isinstance(payload, dict):
            return jsonify({"error": "A JSON object is required"}), 400

        clinical_data = ClinicalDataCreate(**payload)

    except ValidationError as error:
        return (
            jsonify(
                {
                    "error": "Invalid clinical data",
                    "details": error.errors(include_context=False),
                }
            ),
            400,
        )

    db: Session = g.db

    db_item = ClinicalData(
        patient_name=clinical_data.patient_name,
        age=clinical_data.age,
        diagnosis=clinical_data.diagnosis,
        blood_pressure=clinical_data.blood_pressure,
        heart_rate=clinical_data.heart_rate,
        body_temperature=clinical_data.body_temperature,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Convert the saved record into JSON-compatible data
    file_record = db_item.to_dict()

    # Append the same record to the JSON Lines file
    append_to_file(file_record)

    return jsonify(file_record), 201


# GET: Retrieve all clinical records
@app.route("/clinical/", methods=["GET"])
def read_records():
    db: Session = g.db

    records = db.query(ClinicalData).all()

    return jsonify([record.to_dict() for record in records]), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
