from flask import Flask, jsonify, request
from database import db
from repository import (
    CalendarRepository,
    CourseRepository,
    ActivityRepository,
    SectionRepository,
    MetadataRepository,
    EventRepository,
)


class LMSKApi:
    """
    Main API class for the LMSK Scraper.
    Handles Flask initialization, configuration, database setup, and route registration.
    """

    def __init__(self):
        self.app = Flask(__name__)
        self.setup_config()
        self.setup_database()
        self.setup_routes()

    def setup_config(self):
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lmsk.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def setup_database(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def setup_routes(self):
        @self.app.get("/")
        def index():
            return jsonify({"message": "Welcome to fasnet LMS Scraper.!"})

        # Metadata Routes
        @self.app.get("/lmsk/metadata")
        def get_metadatas():
            metadata = MetadataRepository.get_all()
            return jsonify([item.to_dict() for item in metadata])

        @self.app.get("/lmsk/metadata/<int:id>")
        def get_metadata(id):
            metadata = MetadataRepository.get_by_id(id)
            if metadata:
                return jsonify(metadata.to_dict())
            return jsonify({"error": "Metadata not found"}), 404

        @self.app.post("/lmsk/metadata")
        def post_metadata():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data format"}), 400

            try:
                processed_items = MetadataRepository.create(data)
                return jsonify([item.to_dict() for item in processed_items]), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

        # Course Routes
        @self.app.get("/lmsk/course")
        def get_courses():
            courses = CourseRepository.get_all()
            return jsonify([item.to_dict() for item in courses])

        @self.app.get("/lmsk/course/<int:id>")
        def get_course(id):
            course = CourseRepository.get_by_id(id)
            if course:
                return jsonify(course.to_dict())
            return jsonify({"error": "Course not found"}), 404

        @self.app.post("/lmsk/course")
        def post_course():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data format"}), 400

            try:
                processed_items = CourseRepository.create(data)
                return jsonify([item.to_dict() for item in processed_items]), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

        @self.app.put("/lmsk/course/<int:id>")
        def update_course(id):
            data = request.get_json()
            course = CourseRepository.update(id, data)
            if course:
                return jsonify(course.to_dict())
            return jsonify({"error": "Course not found"}), 404

        @self.app.delete("/lmsk/course/<int:id>")
        def delete_course(id):
            if CourseRepository.delete(id):
                return jsonify({"message": "Course deleted successfully"})
            return jsonify({"error": "Course not found"}), 404

        # Activity Routes
        @self.app.get("/lmsk/activity")
        def get_activities():
            activities = ActivityRepository.get_all()
            return jsonify([item.to_dict() for item in activities])

        @self.app.get("/lmsk/activity/<int:id>")
        def get_activity(id):
            activity = ActivityRepository.get_by_id(id)
            if activity:
                return jsonify(activity.to_dict())
            return jsonify({"error": "Activity not found"}), 404

        @self.app.post("/lmsk/activity")
        def post_activity():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data format"}), 400

            try:
                processed_items = ActivityRepository.create(data)
                return jsonify([item.to_dict() for item in processed_items]), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

        @self.app.put("/lmsk/activity/<int:id>")
        def update_activity(id):
            data = request.get_json()
            activity = ActivityRepository.update(id, data)
            if activity:
                return jsonify(activity.to_dict())
            return jsonify({"error": "Activity not found"}), 404

        @self.app.delete("/lmsk/activity/<int:id>")
        def delete_activity(id):
            if ActivityRepository.delete(id):
                return jsonify({"message": "Activity deleted successfully"})
            return jsonify({"error": "Activity not found"}), 404

        # Section Routes
        @self.app.get("/lmsk/section")
        def get_sections():
            sections = SectionRepository.get_all()
            return jsonify([item.to_dict() for item in sections])

        @self.app.get("/lmsk/section/<int:id>")
        def get_section(id):
            section = SectionRepository.get_by_id(id)
            if section:
                return jsonify(section.to_dict())
            return jsonify({"error": "Section not found"}), 404

        @self.app.post("/lmsk/section")
        def post_section():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data format"}), 400

            try:
                processed_items = SectionRepository.create(data)
                return jsonify([item.to_dict() for item in processed_items]), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

        @self.app.put("/lmsk/section/<int:id>")
        def update_section(id):
            data = request.get_json()
            section = SectionRepository.update(id, data)
            if section:
                return jsonify(section.to_dict())
            return jsonify({"error": "Section not found"}), 404

        @self.app.delete("/lmsk/section/<int:id>")
        def delete_section(id):
            if SectionRepository.delete(id):
                return jsonify({"message": "Section deleted successfully"})
            return jsonify({"error": "Section not found"}), 404

        # Calender Routes
        @self.app.get("/lmsk/calender")
        def get_calendars():
            calendars = CalendarRepository.get_all()
            return jsonify([item.to_dict() for item in calendars])

        @self.app.get("/lmsk/calender/<int:id>")
        def get_calendar(id):
            calendar = CalendarRepository.get_by_id(id)
            if calendar:
                return jsonify(calendar.to_dict())
            return jsonify({"error": "Calendar not found"}), 404

        @self.app.post("/lmsk/calender")
        def post_calendar():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data format"}), 400

            try:
                processed_items = CalendarRepository.create(data)
                return jsonify([item.to_dict() for item in processed_items]), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

        @self.app.put("/lmsk/calender/<int:id>")
        def update_calendar(id):
            data = request.get_json()
            calendar = CalendarRepository.update(id, data)
            if calendar:
                return jsonify(calendar.to_dict())
            return jsonify({"error": "Calendar not found"}), 404

        @self.app.delete("/lmsk/calender/<int:id>")
        def delete_calendar(id):
            if CalendarRepository.delete(id):
                return jsonify({"message": "Calendar deleted successfully"})
            return jsonify({"error": "Calendar not found"}), 404

        # Event Routes
        @self.app.get("/lmsk/event")
        def get_events():
            events = EventRepository.get_all()
            return jsonify([item.to_dict() for item in events])

        @self.app.post("/lmsk/event")
        def post_event():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data format"}), 400

            try:
                processed_items = EventRepository.create(data)
                return jsonify([item.to_dict() for item in processed_items]), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

    def run(self, debug=True):
        self.app.run(debug=debug, host="0.0.0.0")


if __name__ == "__main__":
    api = LMSKApi()
    api.run()
