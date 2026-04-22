from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create Database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lmsk.db"

db = SQLAlchemy(app)


class Calendar(db.Model):
    __tablename__ = "calendar"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    last_modified = db.Column(db.String(100), nullable=True)
    dt_stamp = db.Column(db.String(100), nullable=True)
    dt_start = db.Column(db.String(100), nullable=True)
    dt_end = db.Column(db.String(100), nullable=True)
    categories = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "summary": self.summary,
            "description": self.description,
            "last_modified": self.last_modified,
            "dt_stamp": self.dt_stamp,
            "dt_start": self.dt_start,
            "dt_end": self.dt_end,
            "categories": self.categories,
        }


# CREATE ALL TABLES
with app.app_context():
    db.create_all()

# Create Routes


# https://localhost:5000/
@app.get("/")
def index():
    return jsonify({"message": "Welcome to fasnet LMS Scraper.!"})


# https://localhost:5000/lmsk/calender
@app.get("/lmsk/calender")
def get_calendars():
    calendar = Calendar.query.all()

    return jsonify([item.to_dict() for item in calendar])


# https://localhost:5000/lmsk/calender/2
@app.get("/lmsk/calender/<int:id>")
def get_calender(id):
    calendar = Calendar.query.get(id)
    if calendar:
        return jsonify(calendar.to_dict())
    else:
        return jsonify({"error": "Calendar not found"}), 404


# POST
@app.post("/lmsk/calender")
def post_calendar():
    data = request.get_json()
    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, list):
        pass
    else:
        return jsonify({"error": "Invalid data format"}), 400

    try:
        processed_items = []
        for item in data:
            # Create new record if uid is not exist
            uid = item.get("uid")
            if uid:
                calendar = Calendar.query.get(uid)
                if calendar:
                    continue

            new_calendar = Calendar(
                uid=uid,
                summary=item.get("summary"),
                description=item.get("description"),
                last_modified=item.get("last_modified"),
                dt_stamp=item.get("dt_stamp"),
                dt_start=item.get("dt_start"),
                dt_end=item.get("dt_end"),
                categories=item.get("categories"),
            )
            db.session.add(new_calendar)
            processed_items.append(new_calendar)

        db.session.commit()
        return jsonify([item.to_dict() for item in processed_items]), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# PUT
@app.put("/lmsk/calender/<int:id>")
def update_calender(id):
    data = request.get_json()
    calendar = Calendar.query.get(id)
    if calendar:
        calendar.uid = data.get("uid", calendar.uid)
        calendar.summary = data.get("summary", calendar.summary)
        calendar.description = data.get("description", calendar.description)
        calendar.last_modified = data.get("last_modified", calendar.last_modified)
        calendar.dt_stamp = data.get("dt_stamp", calendar.dt_stamp)
        calendar.dt_start = data.get("dt_start", calendar.dt_start)
        calendar.dt_end = data.get("dt_end", calendar.dt_end)
        calendar.categories = data.get("categories", calendar.categories)
        db.session.commit()
        return jsonify(calendar.to_dict())
    else:
        return jsonify({"error": "Calendar not found"}), 404


# DELETE
@app.delete("/lmsk/calender/<int:id>")
def delete_calender(id):
    calendar = Calendar.query.get(id)
    if calendar:
        db.session.delete(calendar)
        db.session.commit()
        return jsonify({"message": "Calendar deleted successfully"})
    else:
        return jsonify({"error": "Calendar not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
