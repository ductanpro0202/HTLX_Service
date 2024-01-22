from flask import Blueprint, render_template, request, redirect, url_for
from app.models.User import User
from extension import db  # Import User model từ file models.py

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Tạo một đối tượng User từ dữ liệu nhập vào
        new_user = User(UserName=username, Email=email, PassWord=password)

        # Lưu đối tượng User vào cơ sở dữ liệu
        new_user.save()  # Gọi method save() trên đối tượng User để lưu vào DB

        # Sau khi đăng ký thành công, chuyển hướng người dùng đến trang chủ hoặc trang đăng nhập
        return redirect(url_for('login'))  # Chuyển hướng đến route home

    # Nếu là method GET, render template cho trang đăng ký
    return render_template('Register.html')
