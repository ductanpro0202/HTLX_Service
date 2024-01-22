from flask import Flask, render_template, redirect, url_for, request
from config import Config
from app.models.User import User, db
from app.service.UserService import server_bp
from app.service.StudentService import student_bp as student_service_bp
from app.routes.Login import login_bp
from app.routes.Register import register_bp
from app.routes.Student import student_bp
from app.routes.Grade import grade_bp
from app.service.GradeService import grade_bp as grade_service_bp
from app.service.InfoStudentService import combine_bp
from app.routes.Department import department_bp
from app.service.DepartmentService import department_service_bp
from app.service.MajorsService import majors_bp as  majors_service_bp
from app.routes.Majors import majors_bp 
from app.routes.Class import class_bp
from app.service.ClassService import class_bp as class_service_bp
from app.routes.Course import course_bp
from app.service.CourseService import course_bp as course_service_bp
# from flask import jsonify
from flask_jwt_extended import JWTManager
# from flask_jwt_extended import jwt_required


app = Flask(__name__, template_folder='app/templates')
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = 'kx123'
db.init_app(app)
app.register_blueprint(server_bp, url_prefix='/api')
app.register_blueprint(student_service_bp, url_prefix='/api/student')
app.register_blueprint(combine_bp, url_prefix='/api/combine')
app.register_blueprint(grade_service_bp, url_prefix='/api/grade')
app.register_blueprint(majors_service_bp, url_prefix='/api/majors')
app.register_blueprint(class_service_bp, url_prefix='/api/class')
app.register_blueprint(department_service_bp, url_prefix='/api/department')
app.register_blueprint(course_service_bp, url_prefix='/api/course')
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(student_bp)
app.register_blueprint(grade_bp)
app.register_blueprint(department_bp)
app.register_blueprint(class_bp)
app.register_blueprint(majors_bp)
app.register_blueprint(course_bp)

jwt = JWTManager(app)
# jwt.init_app(app)

@app.route('/')
def Login():
    return render_template('Login.html')

@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_bp.register()

@app.route('/login', methods=['GET', 'POST'])

def login():
    return login_bp.process_login()

# Route xử lý sinh viên
@app.route('/student', methods=['GET', 'POST'])
def student():
    return student_bp.student()

@app.route('/delete_student/<int:studentID>', methods=['DELETE'])
def delete_student(studentID):
    return student_bp.delete_student()

# Route để trả về thông tin sinh viên dưới dạng JSON để sử dụng trong JavaScript
@app.route('/edit_student/<int:studentID>/json', methods=['GET'])
def edit_student_json(studentID):
    return student_bp.edit_student_json()

@app.route('/edit_student', methods=['PUT'])
def edit_student():
    return student_bp.edit_student()

# xử lý điểm
@app.route('/grade', methods=['GET', 'POST'])
def grade():
    return grade_bp.grade()

     
@app.route('/delete_grade/<int:gradeID>', methods=['POST'])
def delete_grade(gradeID):
    return grade_bp.delete_grade()



@app.route('/edit_grade/<int:gradeID>/json', methods=['GET'])
def edit_grade_json(gradeID):
    return grade_bp.edit_grade_json()

@app.route('/edit_grade', methods=['PUT'])
def edit_grade():
    return grade_bp.edit_grade() 

# sử lý class 
@app.route('/class', methods=['GET', 'POST'])
def classs():
    return class_bp.classs()

@app.route('/delete_class/<classID>', methods=['DELETE'])
def delete_class(classID):
    return class_bp.delete_class()

# Route để trả về thông tin sinh viên dưới dạng JSON để sử dụng trong JavaScript
@app.route('/edit_class/<classID>/json', methods=['GET'])
def edit_class_json(classID):
    return class_bp.edit_class_json()
    

@app.route('/edit_class', methods=['PUT'])
def edit_class():
    return class_bp.edit_class()

# xử lý khoa
@app.route('/majors', methods=['GET', 'POST'])
def majors():
    return class_bp.classs()

@app.route('/delete_majors/<majorsID>', methods=['DELETE'])
def delete_majors(classID):
    return majors_bp.delete_majors()

# Route để trả về thông tin sinh viên dưới dạng JSON để sử dụng trong JavaScript
@app.route('/edit_majors/<majorsID>/json', methods=['GET'])
def edit_majors_json(majorsID):
    return majors_bp.edit_majors_json()
    


@app.route('/edit_majors', methods=['PUT'])
def edit_majors():
    return majors_bp.edit_majors()

# sử lý ngành
@app.route('/department', methods=['GET', 'POST'])
def department():
    return department_bp.department()

@app.route('/delete_department/<departmentID>', methods=['DELETE'])
def delete_department(departmentID):
    return department_bp.delete_department()


@app.route('/edit_department/<departmentID>/json', methods=['GET'])
def edit_department_json(departmentID):
    return department_bp.edit_department_json()
    



@app.route('/edit_department', methods=['PUT'])
def edit_department():
    return department_bp.edit_department()

# sử lý điểm
@app.route('/course', methods=['GET', 'POST'])
def course():
    return course_bp.course()

@app.route('/delete_course/<courseID>', methods=['DELETE'])
def delete_course(courseID):
    return course_bp.delete_course()


@app.route('/edit_course/<courseID>/json', methods=['GET'])
def edit_course_json(courseID):
    return course_bp.edit_course_json()
    


@app.route('/edit_course', methods=['PUT'])
def edit_course():
    return course_bp.edit_course()
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)