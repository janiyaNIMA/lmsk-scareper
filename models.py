from database import db


class Metadata(db.Model):
    __tablename__ = "metadata"

    id = db.Column(db.Integer, primary_key=True)
    scraped_at = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "scraped_at": self.scraped_at,
            "source": self.source,
        }


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


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=True)

    # Relationships
    sections = db.relationship(
        "Sections", backref="course", cascade="all, delete-orphan"
    )
    activities = db.relationship(
        "Activities", backref="course", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "sections": [s.to_dict() for s in self.sections],
        }


class Sections(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Relationships
    activities = db.relationship(
        "Activities", backref="section", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "activities": [a.to_dict() for a in self.activities],
        }


class Activities(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=False)
    activity_type = db.Column(db.String(200), nullable=False)
    activity_name = db.Column(db.String(200), nullable=False)
    resource_url = db.Column(db.String(200), nullable=False)
    info = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "section_id": self.section_id,
            "activity_type": self.activity_type,
            "activity_name": self.activity_name,
            "resource_url": self.resource_url,
            "info": self.info,
        }

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=True)
    course_name = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "course_name": self.course_name,
            "due_date": self.due_date,
        }
