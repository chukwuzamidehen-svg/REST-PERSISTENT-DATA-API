# REST Persistent Data API

## Project Overview

This project is a RESTful clinical records API developed using Python, Flask, SQLAlchemy, Pydantic, and SQLite for the INFO-U762 Interoperability course at USC Upstate.

The application allows users to create and retrieve clinical records through HTTP requests while maintaining persistent data storage.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/clinical/` | Creates and stores a clinical record |
| GET | `/clinical/` | Retrieves all stored clinical records |

## Clinical Record Fields

Each record contains the following fields:

- `id` — Automatically generated record identifier
- `patient_name` — Patient's name
- `age` — Patient's age
- `diagnosis` — Clinical diagnosis
- `blood_pressure` — Additional field
- `heart_rate` — Additional field
- `body_temperature` — Additional field, measured in Fahrenheit
- `recorded_at` — Automatically generated timestamp

## Running the Application

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python main.py
```

The API runs locally at `http://127.0.0.1:8000`.

## Persistent Storage

Records are stored in two formats:

1. **SQLite:** `clinical_data.db`
2. **JSON Lines:** `data/clinical_data.jsonl`

Each successful POST request inserts a record into SQLite and appends a corresponding JSON object to the JSONL file.

## Testing

The API was tested using `curl` commands to create and retrieve fictional patient records using the names of U.S. presidents. All diagnoses and vital signs are fictional.

## Reflection

Building this API helped me better understand how RESTful services handle persistent data rather than simply returning JSON responses. I used SQLAlchemy to manage SQLite, Pydantic to validate incoming records, and Flask to connect everything through POST and GET endpoints. I also extended the original clinical model with three additional fields: blood pressure, heart rate, and body temperature.

One of my biggest challenges actually came before writing much of the code. I had trouble installing the required dependencies, particularly SQLAlchemy. Although the installation initially appeared successful, Windows Application Control blocked one of its compiled extensions. I tried adjusting the environment settings, but the error persisted. Eventually, I had to uninstall SQLAlchemy and reinstall a compatible version from source without the compiled extensions.

Once that issue was resolved, testing the API with curl was fairly straightforward. Using fictional patient records, I confirmed that the application could save information to both SQLite and JSON Lines and retrieve it afterward. This experience reinforced how much troubleshooting and dependency management matter when building interoperable applications.
