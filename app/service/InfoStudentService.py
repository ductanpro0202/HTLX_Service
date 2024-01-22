from flask import Flask, jsonify, request, Blueprint
from app.service.StudentService import get_student
from app.service.GradeService import get_grade

combine_bp = Blueprint('combine', __name__)

# Route để lấy thông tin sinh viên bao gồm điểm
@combine_bp.route('/combine/<int:student_id>', methods=['GET'])
def get_combined_info(student_id):
    # Lấy thông tin sinh viên từ dịch vụ sinh viên
    student_info = get_student(student_id)

    if not student_info:
        return jsonify({'message': 'Không tìm thấy thông tin sinh viên'}), 404

    # Lấy thông tin điểm từ dịch vụ điểm
    grade_info = get_grade(student_id)

    if not grade_info:
        return jsonify({'message': 'Không tìm thấy thông tin điểm sinh viên'}), 404

    # Tính tuổi từ ngày sinh
    # Đây chỉ là một ví dụ, bạn có thể thêm logic phức tạp hơn nếu cần
    birth_year = int(student_info['DOB'][:4])
    current_year = 2024  # Năm hiện tại
    age = current_year - birth_year

    # Tạo thông tin kết hợp
    combined_info = {
        'StudentID': student_info['StudentID'],
        'FullName': student_info['FullName'],
        'DOB': student_info['DOB'],
        'Gender': student_info['Gender'],
        'Email': student_info['Email'],
        'PhoneNumber': student_info['PhoneNumber'],
        'Address': student_info['Address'],
        'ClassID': student_info['ClassID'],
        'Age': age,  # Tuổi được tính từ ngày sinh
        'GradeInfo': {
            'MidtermScore': grade_info['MidtermScore'],
            'Attendance': grade_info['Attendance'],
            'FinalScore': grade_info['FinalScore'],
            'SchoolYear': grade_info['SchoolYear'],
            'Semester': grade_info['Semester']
        }
    }

    return jsonify(combined_info), 200


