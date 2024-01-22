from flask import request, jsonify, redirect, url_for, render_template, Blueprint
from extension import db
from app.models.Department import Department  # Update with the actual module name

department_bp = Blueprint('department_bp', __name__)

@department_bp.route('/department', methods=['GET', 'POST'])
def departments():
    if request.method == 'POST':
        departmentID = request.form['departmentID']
        departmentName = request.form['departmentName']

        # Check if the department already exists
        existing_department = Department.query.filter_by(departmentID=departmentID).first()
        if existing_department:
            return jsonify({'message': 'Phòng ban đã tồn tại'}), 400

        new_department = Department(departmentID=departmentID, departmentName=departmentName)
        db.session.add(new_department)
        db.session.commit()

        return redirect(url_for('department'))

    departments = Department.query.all()
    return render_template('Department.html', departments=departments)

@department_bp.route('/delete_department/<departmentID>', methods=['POST'])
def delete_department(departmentID):
    department = Department.query.get(departmentID)
    if department:
        db.session.delete(department)
        db.session.commit()
    return redirect(url_for('department'))

@department_bp.route('/edit_department/<departmentID>/json', methods=['GET'])
def edit_department_json(departmentID):
    department = Department.query.get(departmentID)
    if department:
        department_data = {
            'departmentID': department.departmentID,
            'departmentName': department.departmentName,
            # Additional fields if needed
        }
        return jsonify(department_data)
    return jsonify({'message': 'Không tìm thấy phòng ban'})

@department_bp.route('/edit_department/<departmentID>', methods=['PUT'])
def edit_department(departmentID):
    data = request.get_json()

    department = Department.query.filter_by(departmentID=departmentID).first()

    if department:
        department.departmentName = data.get('departmentName')
        # Update additional fields if needed
        db.session.commit()
        return jsonify({'message': 'Cập nhật phòng ban thành công'})

    return jsonify({'message': 'Không tìm thấy phòng ban'}), 404
