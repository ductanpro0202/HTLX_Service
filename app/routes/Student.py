from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.Student import SinhVien
from extension import db

student_bp = Blueprint('student_bp', __name__)

# Route để hiển thị danh sách sinh viên và thêm sinh viên mới
@student_bp.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        student_id = request.form['studentID']
        full_name = request.form['fullName']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone_number = request.form['phoneNumber']
        address = request.form['address']
        class_id = request.form['classID']

        # Kiểm tra xem sinh viên có tồn tại chưa
        existing_student = SinhVien.query.filter_by(studentID=student_id).first()
        if existing_student:
            return jsonify({'message': 'Sinh viên với mã sinh viên đã tồn tại'}), 400

        # Tạo một đối tượng sinh viên và lưu vào cơ sở dữ liệu
        new_student = SinhVien(
            studentID=student_id,
            fullName=full_name,
            dob=dob,
            gender=gender,
            email=email,
            phoneNumber=phone_number,
            address=address,
            classID=class_id
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('student'))

    # Nếu là GET request, hiển thị form quản lý sinh viên
    students = SinhVien.query.all()
    return render_template('Student.html', students=students)

@student_bp.route('/delete_student/<int:studentID>', methods=['DELETE'])
def delete_student(studentID):
    student = SinhVien.query.get(studentID)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Xóa sinh viên thành công'})
    return jsonify({'message': 'Không tìm thấy sinh viên'})

# Route để trả về thông tin sinh viên dưới dạng JSON để sử dụng trong JavaScript
@student_bp.route('/edit_student/<int:studentID>/json', methods=['GET'])
def edit_student_json(studentID):
    student = SinhVien.query.get(studentID)
    if student:
        student_data = {
            'studentID':student.studentID,
            'fullName': student.fullName,
            'dob': str(student.dob),
            'gender': student.gender,
            'email': student.email,
            'phoneNumber': student.phoneNumber,
            'address': student.address,
            'classID': student.classID
        }
        return jsonify(student_data)
    return jsonify({'message': 'Không tìm thấy sinh viên'}), 404
@student_bp.route('/edit_student', methods=['PUT'])
def edit_student():
    data = request.get_json()  # Lấy dữ liệu từ yêu cầu JSON
    student_id = data.get('studentID')

    # Kiểm tra xem sinh viên có tồn tại không
    student = SinhVien.query.get(student_id)
    if student:
        # Cập nhật thông tin sinh viên
        student.fullName = data.get('fullName')
        student.dob = data.get('dob')
        student.gender = data.get('gender')
        student.email = data.get('email')
        student.phoneNumber = data.get('phoneNumber')
        student.address = data.get('address')
        student.classID = data.get('classID')

        db.session.commit()
        return jsonify({'message': 'Cập nhật sinh viên thành công'})

    return jsonify({'message': 'Không tìm thấy sinh viên'}), 404

# @student_bp.route('/edit_student', methods=['POST'])


# ... (phần còn lại của mã nguồn vẫn giữ nguyên)
