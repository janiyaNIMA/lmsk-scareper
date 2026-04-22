from database import db
from models import Calendar, Course, Sections, Activities


class CalendarRepository:
    """
    Handles all database operations for the Calendar entity.
    Encapsulates CRUD logic and validation (e.g., duplicate UID check).
    """
    @staticmethod
    def get_all():
        return Calendar.query.all()

    @staticmethod
    def get_by_id(calendar_id):
        return Calendar.query.get(calendar_id)

    @staticmethod
    def get_by_uid(uid):
        return Calendar.query.filter_by(uid=uid).first()

    @staticmethod
    def create(data):
        if isinstance(data, dict):
            data = [data]

        processed_items = []
        for item in data:
            uid = item.get("uid")
            if uid:
                existing = CalendarRepository.get_by_uid(uid)
                if existing:
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
        return processed_items

    @staticmethod
    def update(calendar_id, data):
        calendar = Calendar.query.get(calendar_id)
        if not calendar:
            return None

        calendar.uid = data.get("uid", calendar.uid)
        calendar.summary = data.get("summary", calendar.summary)
        calendar.description = data.get("description", calendar.description)
        calendar.last_modified = data.get("last_modified", calendar.last_modified)
        calendar.dt_stamp = data.get("dt_stamp", calendar.dt_stamp)
        calendar.dt_start = data.get("dt_start", calendar.dt_start)
        calendar.dt_end = data.get("dt_end", calendar.dt_end)
        calendar.categories = data.get("categories", calendar.categories)

        db.session.commit()
        return calendar

    @staticmethod
    def delete(calendar_id):
        calendar = Calendar.query.get(calendar_id)
        if not calendar:
            return False

        db.session.delete(calendar)
        db.session.commit()
        return True


class CourseRepository:
    """
    Handles all database operations for the Course entity.
    Provides methods for CRUD operations and retrieval by name.
    """
    @staticmethod
    def get_all():
        return Course.query.all()

    @staticmethod
    def get_by_id(course_id):
        return Course.query.get(course_id)

    @staticmethod
    def get_by_name(name):
        return Course.query.filter_by(name=name).first()

    @staticmethod
    def create(data):
        if isinstance(data, dict):
            data = [data]

        processed_items = []
        for item in data:
            name = item.get("name")
            if name:
                existing = CourseRepository.get_by_name(name)
                if existing:
                    continue

            new_course = Course(
                name=name,
                full_name=item.get("full_name"),
            )
            db.session.add(new_course)
            processed_items.append(new_course)

        db.session.commit()
        return processed_items

    @staticmethod
    def update(course_id, data):
        course = Course.query.get(course_id)
        if not course:
            return None

        course.name = data.get("name", course.name)
        course.full_name = data.get("full_name", course.full_name)

        db.session.commit()
        return course

    @staticmethod
    def delete(course_id):
        course = Course.query.get(course_id)
        if not course:
            return False

        db.session.delete(course)
        db.session.commit()
        return True


class ActivityRepository:
    """
    Handles all database operations for Activities.
    Manages relationships between Courses, Sections, and Activities.
    """
    @staticmethod
    def get_all():
        return Activities.query.all()

    @staticmethod
    def get_by_id(activity_id):
        return Activities.query.get(activity_id)

    @staticmethod
    def get_by_name(activity_name):
        return Activities.query.filter_by(activity_name=activity_name).first()

    @staticmethod
    def create(data):
        if isinstance(data, dict):
            data = [data]

        processed_items = []
        for item in data:
            activity_name = item.get("activity_name")
            if activity_name:
                existing = ActivityRepository.get_by_name(activity_name)
                if existing:
                    continue

            new_activity = Activities(
                course_id=item.get("course_id"),
                section_id=item.get("section_id"),
                activity_type=item.get("activity_type"),
                activity_name=activity_name,
                resource_url=item.get("resource_url"),
                info=item.get("info")
            )
            db.session.add(new_activity)
            processed_items.append(new_activity)

        db.session.commit()
        return processed_items

    @staticmethod
    def update(activity_id, data):
        activity = Activities.query.get(activity_id)
        if not activity:
            return None

        activity.activity_name = data.get("activity_name", activity.activity_name)
        activity.activity_type = data.get("activity_type", activity.activity_type)
        activity.resource_url = data.get("resource_url", activity.resource_url)
        activity.info = data.get("info", activity.info)

        db.session.commit()
        return activity

    @staticmethod
    def delete(activity_id):
        activity = Activities.query.get(activity_id)
        if not activity:
            return False

        db.session.delete(activity)
        db.session.commit()
        return True


class SectionRepository:
    """
    Handles all database operations for Sections.
    """
    @staticmethod
    def get_all():
        return Sections.query.all()

    @staticmethod
    def get_by_id(section_id):
        return Sections.query.get(section_id)

    @staticmethod
    def get_by_title(title):
        return Sections.query.filter_by(title=title).first()

    @staticmethod
    def create(data):
        if isinstance(data, dict):
            data = [data]

        processed_items = []
        for item in data:
            title = item.get("title")
            if title:
                existing = SectionRepository.get_by_title(title)
                if existing:
                    continue

            new_section = Sections(
                course_id=item.get("course_id"),
                title=title,
            )
            db.session.add(new_section)
            processed_items.append(new_section)

        db.session.commit()
        return processed_items

    @staticmethod
    def update(section_id, data):
        section = Sections.query.get(section_id)
        if not section:
            return None

        section.title = data.get("title", section.title)

        db.session.commit()
        return section

    @staticmethod
    def delete(section_id):
        section = Sections.query.get(section_id)
        if not section:
            return False

        db.session.delete(section)
        db.session.commit()
        return True
