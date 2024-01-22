from flask import Blueprint, jsonify, request
from app.models.Course import Course  # Assuming you have a Course model
from extension import db

course_bp = Blueprint('course', __name__)

# Create a new course
@course_bp.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()

    # Check if the course with the given courseID already exists
    existing_course = Course.query.filter_by(courseID=data['courseID']).first()
    if existing_course:
        return jsonify({'message': 'Mã môn học đã tồn tại'}), 400

    # Continue creating the course if the courseID does not exist
    new_course = Course(courseID=data['courseID'], courseName=data['courseName'], credits=data['credits'])

    db.session.add(new_course)
    db.session.commit()

    return jsonify({'message': 'Môn học được tạo thành công'}), 201

# Get all courses
@course_bp.route('/course', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    course_list = [{'CourseID': course.courseID, 'CourseName': course.courseName,
                    'Credits': course.credits} for course in courses]
    return jsonify({'courses': course_list})

# Get a specific course by ID
@course_bp.route('/course/<string:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)

    if course:
        course_info = {'CourseID': course.courseID, 'CourseName': course.courseName,
                       'Credits': course.credits}
        return jsonify({'course': course_info})

    return jsonify({'message': 'Course not found'}), 404

# Update a course by ID
@course_bp.route('/course/<string:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get(course_id)

    if course:
        data = request.get_json()
        course.courseName = data.get('courseName', course.courseName)
        course.credits = data.get('credits', course.credits)

        db.session.commit()

        return jsonify({'message': 'Course updated successfully'})

    return jsonify({'message': 'Course not found'}), 404

# Delete a course by ID
@course_bp.route('/course/<string:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)

    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': 'Course deleted successfully'})

    return jsonify({'message': 'Course not found'}), 404
