from flask import request, jsonify, Blueprint
from app.models.Majors import Majors
from app.models.Department import Department  # Import the Department model
from extension import db

majors_bp = Blueprint('majors', __name__)

# Create a new Majors
@majors_bp.route('/majors', methods=['POST'])
def create_majors():
    data = request.get_json()

    # Check if the majors with the given majorsID exists
    existing_majors = Majors.query.filter_by(majorsID=data['majorsID']).first()
    if existing_majors:
        return jsonify({'message': 'Majors already exists'}), 400

    # Check if the department_id exists in the Department table
    existing_department = Department.query.filter_by(departmentID=data['department_id']).first()
    if not existing_department:
        return jsonify({'message': 'Department does not exist'}), 400

    # Continue creating the majors since it doesn't exist
    new_majors = Majors(
        majorsID=data['majorsID'],
        majorsName=data['majorsName'],
        department_id=data['department_id']
    )

    db.session.add(new_majors)
    db.session.commit()

    return jsonify({'message': 'Majors created successfully'}), 201

# Get all majors
@majors_bp.route('/majors', methods=['GET'])
def get_all_majors():
    majors = Majors.query.all()
    majors_list = [{'MajorsID': major.majorsID, 'MajorsName': major.majorsName,
                    'DepartmentID': major.department_id} for major in majors]
    return jsonify({'majors': majors_list})

# Get a specific majors by ID
@majors_bp.route('/majors/<majors_id>', methods=['GET'])
def get_majors(majors_id):
    majors = Majors.query.get(majors_id)

    if majors:
        majors_info = {'MajorsID': majors.majorsID, 'MajorsName': majors.majorsName,
                       'DepartmentID': majors.department_id}
        return jsonify({'majors': majors_info})

    return jsonify({'message': 'Majors not found'}), 404

# Update a majors by ID
@majors_bp.route('/edit_majors', methods=['PUT'])
def update_majors():
    data = request.get_json()
    majors = Majors.query.get(data['majorsID'])

    if majors:
        majors.majorsName = data.get('majorsName', majors.majorsName)
        majors.department_id = data.get('department_id', majors.department_id)

        db.session.commit()

        return jsonify({'message': 'Majors updated successfully'})

    return jsonify({'message': 'Majors not found'}), 404

# Delete a majors by ID
@majors_bp.route('/delete_majors/<majors_id>', methods=['POST'])
def delete_majors(majors_id):
    majors = Majors.query.get(majors_id)

    if majors:
        db.session.delete(majors)
        db.session.commit()
        return jsonify({'message': 'Majors deleted successfully'})

    return jsonify({'message': 'Majors not found'}), 404
