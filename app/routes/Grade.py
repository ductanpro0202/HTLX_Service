from flask import request, jsonify, redirect, url_for, render_template,Blueprint
from extension import db
from app.models.Grade import Grade
from app.models.Course import Course  # Update with the actual module name

grade_bp = Blueprint('grade_bp', __name__)
@grade_bp.route('/grade', methods=['GET', 'POST'])
def grade():
    if request.method == 'POST':
        studentID = request.form['studentID']
        courseID = request.form['courseID']
        midtermScore = request.form['midtermScore']
        attendance = request.form['attendance']
        finalScore = request.form['finalScore']
        schoolYear = request.form['schoolYear']
        semester = request.form['semester']
        averageScore = request.form['averageScore']

        # Kiểm tra xem môn học có tồn tại không
        existing_course = Course.query.filter_by(courseID=courseID).first()
        if not existing_course:
            return jsonify({'message': 'Môn học không tồn tại'}), 400

        # Kiểm tra xem điểm đã tồn tại chưa
        existing_grade = Grade.query.filter_by(studentID=studentID, courseID=courseID).first()
        if existing_grade:
            return jsonify({'message': 'Điểm của sinh viên cho môn học trong học kỳ và năm học đã tồn tại'}), 400

        new_grade = Grade(studentID=studentID, courseID=courseID,
                          midtermScore=midtermScore, attendance=attendance,
                          finalScore=finalScore, schoolYear=schoolYear,
                          semester=semester, averageScore=averageScore)
        db.session.add(new_grade)
        db.session.commit()

        return redirect(url_for('grade'))

    grades = Grade.query.all()
    return render_template('Grade.html', grades=grades)


@grade_bp.route('/delete_grade/<int:gradeID>', methods=['POST'])
def delete_grade(gradeID):
    grade = Grade.query.get(gradeID)
    if grade:
        db.session.delete(grade)
        db.session.commit()
    return redirect(url_for('grade'))
@grade_bp.route('/edit_grade/<int:gradeID>/json', methods=['GET'])
def edit_grade_json(gradeID):
    grade = Grade.query.get(gradeID)
    if grade:
        grade_data = {
            'studentID': grade.studentID,
            'courseID': grade.courseID,
            'midtermScore': grade.midtermScore,
            'attendance': grade.attendance,
            'finalScore': grade.finalScore,
            'averageScore':grade.averageScore,
            'schoolYear': grade.schoolYear,
            'semester': grade.semester
            
        }
        return jsonify(grade_data)
    return jsonify({'message': 'Không tìm thấy điểm'}),
@grade_bp.route('/edit_grade', methods=['PUT'])
def edit_grade():
    data = request.get_json()  # Lấy dữ liệu từ yêu cầu JSON

    # Tìm kiếm điểm dựa trên studentID, courseID, schoolYear, và semester
    grade = Grade.query.filter_by(
        studentID=data.get('studentID'),
        courseID=data.get('courseID'),
        schoolYear=data.get('schoolYear'),
        semester=data.get('semester')
        
    ).first()

    if grade:
        # Cập nhật thông tin điểm
        grade.midtermScore = data.get('midtermScore')
        grade.attendance = data.get('attendance')
        grade.finalScore = data.get('finalScore')
        grade.averageScore=data.get('averageScore')
        db.session.commit()
        return jsonify({'message': 'Cập nhật điểm thành công'})

    return jsonify({'message': 'Không tìm thấy điểm'}), 404


    

