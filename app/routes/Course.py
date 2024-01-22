from flask import request, jsonify, redirect, url_for, render_template, Blueprint
from extension import db
from app.models.Course import Course  # Update with the actual module name

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/course', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        courseID = request.form['courseID']
        courseName = request.form['courseName']
        credits = request.form['credits']

        # kiểm tra môn học đã tồn tại chưa
        existing_course = Course.query.filter_by(courseID=courseID).first()
        if existing_course:
            return jsonify({'message': 'Môn học đã tồn tại'}), 400

        new_course = Course(courseID=courseID, courseName=courseName, credits=credits)
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('course'))

    courses = Course.query.all()
    return render_template('Course.html', courses=courses)

@course_bp.route('/delete_course/<courseID>', methods=['POST'])
def delete_course(courseID):
    course = Course.query.get(courseID)
    if course:
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for('course'))

@course_bp.route('/edit_course/<courseID>/json', methods=['GET'])
def edit_course_json(courseID):
    course = Course.query.get(courseID)
    if course:
        course_data = {
            'courseID': course.courseID,
            'courseName': course.courseName,
            'credits': course.credits,
        }
        return jsonify(course_data)
    return jsonify({'message': 'Không tìm thấy môn học'})

@course_bp.route('/edit_course', methods=['PUT'])
def edit_course():
    data = request.get_json()

    course = Course.query.filter_by(courseID=data.get('courseID')).first()

    if course:
        course.courseName = data.get('courseName')
        course.credits = data.get('credits')
        db.session.commit()
        return jsonify({'message': 'Cập nhật môn học thành công'})

    return jsonify({'message': 'Không tìm thấy môn học'}), 404
