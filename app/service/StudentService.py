from flask import Blueprint, jsonify, request
from app.models.Student import SinhVien
from extension import db

student_bp = Blueprint('student', __name__)


@student_bp.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    student_id = data.get('studentID')  # Giả sử có trường 'studentID' trong dữ liệu JSON

    # Kiểm tra xem mã sinh viên đã tồn tại chưa
    existing_student = SinhVien.query.get(student_id)
    if existing_student:
        return jsonify({'message': 'Sinh viên với mã sinh viên đã tồn tại'}), 400

    new_student = SinhVien(studentID=student_id, fullName=data['fullName'], dob=data['dob'], gender=data['gender'],
                          email=data['email'], phoneNumber=data['phoneNumber'],
                          address=data['address'], classID=data['classID'])

    db.session.add(new_student)
    db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

    return jsonify({'message': 'Sinh viên được tạo thành công'}), 201

# Get all students
@student_bp.route('/student', methods=['GET'])
def get_all_students():
    students = SinhVien.query.all()
    student_list = [{'StudentID': student.studentID, 'FullName': student.fullName, 'DOB': student.dob,
                     'Gender': student.gender, 'Email': student.email, 'PhoneNumber': student.phoneNumber,
                     'Address': student.address, 'ClassID': student.classID} for student in students]
    return jsonify({'students': student_list})

# Get a specific student by ID
@student_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = SinhVien.query.get(student_id)

    if student:
        student_info = {'StudentID': student.studentID, 'FullName': student.fullName, 'DOB': student.dob,
                        'Gender': student.gender, 'Email': student.email, 'PhoneNumber': student.phoneNumber,
                        'Address': student.address, 'ClassID': student.classID}
        return jsonify({'student': student_info})

    return jsonify({'message': 'Student not found'}), 404

# Update a student by ID
@student_bp.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = SinhVien.query.get(student_id)

    if student:
        data = request.get_json()
        student.fullName = data.get('fullName', student.fullName)
        student.dob = data.get('dob', student.dob)
        student.gender = data.get('gender', student.gender)
        student.email = data.get('email', student.email)
        student.phoneNumber = data.get('phoneNumber', student.phoneNumber)
        student.address = data.get('address', student.address)
        student.classID = data.get('classID', student.classID)

        db.session.commit()

        return jsonify({'message': 'Student updated successfully'})

    return jsonify({'message': 'Student not found'}), 404

# Delete a student by ID
@student_bp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = SinhVien.query.get(student_id)

    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'})

    return jsonify({'message': 'Student not found'}), 404
