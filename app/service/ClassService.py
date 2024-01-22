from flask import request, jsonify, Blueprint
from extension import db
from app.models.Class import Class  # Update with the actual module name
from app.models.Majors import Majors  # Import the Majors model

class_bp = Blueprint('class', __name__)

@class_bp.route('/class', methods=['POST'])
def create_class():
    data = request.get_json()

    # Kiểm tra nếu mã lớp đã tồn tại
    existing_class = Class.query.filter_by(className=data['className']).first()
    if existing_class:
        return jsonify({'message': 'Mã lớp đã tồn tại'}), 400

    # Kiểm tra xem mã ngành đã tồn tại trong bảng ngành hay chưa
    existing_majors = Majors.query.filter_by(majorsID=data['majorsID']).first()
    if not existing_majors:
        return jsonify({'message': 'Mã ngành không tồn tại'}), 400

    # Tiếp tục tạo lớp nếu mã lớp và mã ngành đều chưa tồn tại
    new_class = Class(classID= data['classID'],className=data['className'], majorsID=data['majorsID'], classSize=data['classSize'])

    db.session.add(new_class)
    db.session.commit()

    return jsonify({'message': 'Lớp được tạo thành công'}), 201
# Get all classes
@class_bp.route('/class', methods=['GET'])
def get_all_classes():
    classes = Class.query.all()
    class_list = [{'ClassID': _class.classID, 'ClassName': _class.className,
                   'MajorsID': _class.majorsID, 'ClassSize': _class.classSize} for _class in classes]
    return jsonify({'classes': class_list})

# Get a specific class by ID
@class_bp.route('/class/<class_id>', methods=['GET'])
def get_class(class_id):
    _class = Class.query.get(class_id)

    if _class:
        class_info = {'ClassID': _class.classID, 'ClassName': _class.className,
                      'MajorsID': _class.majorsID, 'ClassSize': _class.classSize}
        return jsonify({'class': class_info})

    return jsonify({'message': 'Class not found'}), 404

# Update a class by ID
@class_bp.route('/class/<class_id>', methods=['PUT'])
def update_class(class_id):
    _class = Class.query.get(class_id)

    if _class:
        data = request.get_json()
        _class.className = data.get('className', _class.className)
        _class.majorsID = data.get('majorsID', _class.majorsID)
        _class.classSize = data.get('classSize', _class.classSize)

        db.session.commit()

        return jsonify({'message': 'Class updated successfully'})

    return jsonify({'message': 'Class not found'}), 404

# Delete a class by ID
@class_bp.route('/class/<class_id>', methods=['DELETE'])
def delete_class(class_id):
    _class = Class.query.get(class_id)

    if _class:
        db.session.delete(_class)
        db.session.commit()
        return jsonify({'message': 'Class deleted successfully'})

    return jsonify({'message': 'Class not found'}), 404
