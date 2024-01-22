from flask import request, jsonify, redirect, url_for, render_template, Blueprint
from extension import db
from app.models.Majors import Majors  # Update with the actual module name
from app.models.Department import Department  # Import the Department model

majors_bp = Blueprint('majors_bp', __name__)

@majors_bp.route('/majors', methods=['GET', 'POST'])
def majors():
    if request.method == 'POST':
        majorsID = request.form['majorsID']
        majorsName = request.form['majorsName']
        department_id = request.form['department_id']

        # Kiểm tra ngành học đã tồn tại chưa
        existing_majors = Majors.query.filter_by(majorsID=majorsID).first()
        if existing_majors:
            return jsonify({'message': 'Ngành học đã tồn tại'}), 400

        # Kiểm tra xem mã khoa đã tồn tại trong bảng khoa hay chưa
        existing_department = Department.query.filter_by(departmentID=department_id).first()
        if not existing_department:
            return jsonify({'message': 'Mã khoa không tồn tại'}), 400

        new_majors = Majors(majorsID=majorsID, majorsName=majorsName, department_id=department_id)
        db.session.add(new_majors)
        db.session.commit()

        return redirect(url_for('majors'))

    majors_list = Majors.query.all()
    return render_template('Majors.html', majors=majors_list)

@majors_bp.route('/delete_majors/<majorsID>', methods=['POST'])
def delete_majors(majorsID):
    majors = Majors.query.get(majorsID)
    if majors:
        db.session.delete(majors)
        db.session.commit()
    return redirect(url_for('majors'))

@majors_bp.route('/edit_majors/<majorsID>/json', methods=['GET'])
def edit_majors_json(majorsID):
    majors = Majors.query.get(majorsID)
    if majors:
        majors_data = {
            'majorsID': majors.majorsID,
            'majorsName': majors.majorsName,
            'department_id': majors.department_id,
        }
        return jsonify(majors_data)
    return jsonify({'message': 'Không tìm thấy ngành học'})

@majors_bp.route('/edit_majors', methods=['PUT'])
def edit_majors():
    data = request.get_json()

    majors = Majors.query.filter_by(majorsID=data.get('majorsID')).first()

    if majors:
        majors.majorsName = data.get('majorsName')
        majors.department_id = data.get('department_id')
        db.session.commit()
        return jsonify({'message': 'Cập nhật ngành học thành công'})

    return jsonify({'message': 'Không tìm thấy ngành học'}), 404
