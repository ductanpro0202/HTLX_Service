from flask import request, jsonify, redirect, url_for, render_template, Blueprint
from extension import db
from app.models.Class import Class  
from app.models.Majors import Majors 
class_bp = Blueprint('class_bp', __name__)
@class_bp.route('/class', methods=['GET', 'POST'])
def classs():
    if request.method == 'POST':
        classID = request.form['classID']
        className = request.form['className']
        majorsID = request.form['majorsID']
        classSize = request.form['classSize']

        # Kiểm tra lớp đã tồn tại chưa
        existing_class = Class.query.filter_by(classID=classID).first()
        if existing_class:
            return jsonify({'message': 'Lớp học đã tồn tại'}), 400

        # Kiểm tra xem mã ngành có tồn tại trong bảng ngành hay không
        existing_majors = Majors.query.filter_by(majorsID=majorsID).first()
        if not existing_majors:
            return jsonify({'message': 'Mã ngành không tồn tại'}), 400

        # Tiếp tục tạo lớp nếu không có sự trùng lặp
        new_class = Class(classID=classID, className=className, majorsID=majorsID, classSize=classSize)

        db.session.add(new_class)
        db.session.commit()

        # Chuyển hướng (redirect) sau khi thêm thành công
        return redirect(url_for('classs'))

    # Xử lý GET request, lấy danh sách lớp học và render template
    classes = Class.query.all()
    return render_template('Class.html', classes=classes)



@class_bp.route('/delete_class/<classID>', methods=['POST'])
def delete_class(classID):
    class_ = Class.query.get(classID)
    if class_:
        db.session.delete(class_)
        db.session.commit()
    return redirect(url_for('classs'))

@class_bp.route('/edit_class/<classID>/json', methods=['GET'])
def edit_class_json(classID):
    class_ = Class.query.get(classID)
    if class_:
        class_data = {
            'classID': class_.classID,
            'className': class_.className,
            'majorsID': class_.majorsID,
            'classSize': class_.classSize,
        }
        return jsonify(class_data)
    return jsonify({'message': 'Không tìm thấy lớp học'})

@class_bp.route('/edit_class', methods=['PUT'])
def edit_class():
    data = request.get_json()

    class_ = Class.query.filter_by(classID=data.get('classID')).first()

    if class_:
        class_.className = data.get('className')
        class_.majorsID = data.get('majorsID')
        class_.classSize = data.get('classSize')
        db.session.commit()
        return jsonify({'message': 'Cập nhật lớp học thành công'})

    return jsonify({'message': 'Không tìm thấy lớp học'}), 404
