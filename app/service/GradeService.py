from flask import Blueprint, jsonify, request
from app.models.Grade import Grade  
from app.models.Student import SinhVien
from extension import db

grade_bp = Blueprint('grade', __name__)

# Create a new grade
@grade_bp.route('/grade', methods=['POST'])
def create_grade():
    data = request.get_json()

    # Check if the student with the given studentID exists
    existing_student = SinhVien.query.filter_by(studentID=data['studentID']).first()
    if not existing_student:
        return jsonify({'message': 'Student not found'}), 404

    # Continue creating the grade since the student exists
    new_grade = Grade(studentID=data['studentID'], courseID=data['courseID'],
                      midtermScore=data['midtermScore'], attendance=data['attendance'],
                      finalScore=data['finalScore'],averageScore=data['averageScore'], schoolYear=data['schoolYear'],
                      semester=data['semester'])

    db.session.add(new_grade)
    db.session.commit()

    return jsonify({'message': 'Grade created successfully'}), 201

# Get all grades
@grade_bp.route('/grade', methods=['GET'])
def get_all_grades():
    grades = Grade.query.all()
    grade_list = [{'GradeID': grade.gradeID, 'StudentID': grade.studentID, 'CourseID': grade.courseID,
                   'MidtermScore': grade.midtermScore, 'Attendance': grade.attendance,
                   'FinalScore': grade.finalScore,'AverageScore':grade.averageScore ,'SchoolYear': grade.schoolYear,
                   'Semester': grade.semester} for grade in grades]
    return jsonify({'grades': grade_list})

# Get a specific grade by ID
@grade_bp.route('/grade/<int:grade_id>', methods=['GET'])
def get_grade(grade_id):
    grade = Grade.query.get(grade_id)

    if grade:
        grade_info = {'GradeID': grade.gradeID, 'StudentID': grade.studentID, 'CourseID': grade.courseID,
                      'MidtermScore': grade.midtermScore, 'Attendance': grade.attendance,
                      'FinalScore': grade.finalScore, 'AverageScore':grade.averageScore ,'SchoolYear': grade.schoolYear,
                      'Semester': grade.semester}
        return jsonify({'grade': grade_info})

    return jsonify({'message': 'Grade not found'}), 404

# Update a grade by ID
@grade_bp.route('/grade/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    grade = Grade.query.get(grade_id)

    if grade:
        data = request.get_json()
        grade.studentID = data.get('studentID', grade.studentID)
        grade.courseID = data.get('courseID', grade.courseID)
        grade.midtermScore = data.get('midtermScore', grade.midtermScore)
        grade.attendance = data.get('attendance', grade.attendance)
        grade.finalScore = data.get('finalScore', grade.finalScore)
        grade.averageScore= data.get('averagrScore', grade.averageScore)
        grade.schoolYear = data.get('schoolYear', grade.schoolYear)
        grade.semester = data.get('semester', grade.semester)


        db.session.commit()

        return jsonify({'message': 'Grade updated successfully'})

    return jsonify({'message': 'Grade not found'}), 404

# Delete a grade by ID
@grade_bp.route('/grade/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    grade = Grade.query.get(grade_id)

    if grade:
        db.session.delete(grade)
        db.session.commit()
        return jsonify({'message': 'Grade deleted successfully'})

    return jsonify({'message': 'Grade not found'}), 404
