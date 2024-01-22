from flask import Blueprint, jsonify, request
from app.models.Department import Department  
from extension import db

department_service_bp = Blueprint('department', __name__)

# Create a new department
@department_service_bp.route('/department', methods=['POST'])
def create_department():
    data = request.get_json()

    new_department = Department(departmentID=data['departmentID'], departmentName=data['departmentName'])
    db.session.add(new_department)
    db.session.commit()

    return jsonify({'message': 'Department created successfully'}), 201

# Get all departments
@department_service_bp.route('/department', methods=['GET'])
def get_all_departments():
    departments = Department.query.all()
    department_list = [{'DepartmentID': department.departmentID, 'DepartmentName': department.departmentName}
                       for department in departments]
    return jsonify({'departments': department_list})

# Get a specific department by ID
@department_service_bp.route('/department/<string:department_id>', methods=['GET'])
def get_department(department_id):
    department = Department.query.get(department_id)

    if department:
        department_info = {'DepartmentID': department.departmentID, 'DepartmentName': department.departmentName}
        return jsonify({'department': department_info})

    return jsonify({'message': 'Department not found'}), 404

# Update a department by ID
@department_service_bp.route('/department/<string:department_id>', methods=['PUT'])
def update_department(department_id):
    department = Department.query.get(department_id)

    if department:
        data = request.get_json()
        department.departmentName = data.get('departmentName', department.departmentName)

        db.session.commit()

        return jsonify({'message': 'Department updated successfully'})

    return jsonify({'message': 'Department not found'}), 404

# Delete a department by ID
@department_service_bp.route('/department/<string:department_id>', methods=['DELETE'])
def delete_department(department_id):
    department = Department.query.get(department_id)

    if department:
        db.session.delete(department)
        db.session.commit()
        return jsonify({'message': 'Department deleted successfully'})

    return jsonify({'message': 'Department not found'}), 404
