from flask import Flask, jsonify, render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
app = Flask(__name__)

# # Flask 쉘에서 데이터베이스 조작
# flask shell

# # 데이터베이스 초기화
# db.drop_all()
# db.create_all()

# # 사용자 조회
# User.query.all()

# # 특정 사용자의 이벤트 조회
# user = User.query.first()
# user.events


#db 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # 데이터베이스 URI 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#24비트 랜덤 바이트 비밀키
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)
# 사용자 객체 생성
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#User모델 정의
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(80), primary_key=True)
    # 사용자 식별자, 로그인 ID로 사용
    # String(80): 최대 80자까지 저장 가능
    # primary_key=True: 기본키로 설정, 중복 불가
    password = db.Column(db.String(120), nullable=False)
    # 해시화된 비밀번호 저장
    # String(120): 해시된 비밀번호는 긴 문자열이 필요
    # nullable=False: 필수 입력 필드
    def __repr__(self):
        return f'<User {self.id}>' 
    



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']

        if User.query.filter_by(id=user_id).first():
            flash('이미 존재하는 아이디입니다.')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(id=user_id, password=hashed_password)  # 해시화된 비밀번호 저장

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('회원가입이 완료되었습니다.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('회원가입에 실패하였습니다.')
            return redirect(url_for('register'))
    return render_template('register.html')
        
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id=request.form['id']
        password=request.form['password']

        user=User.query.filter_by(id=user_id).first()
        
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash('로그인이 완료되었습니다.')
            return render_template('index.html')
        flash('아이디 또는 비밀번호가 일치하지 않습니다.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃이 완료되었습니다.')
    return redirect(url_for('index'))



# 데이터베이스 초기화 (처음 한 번만 실행)
@app.before_first_request
def create_tables():
    db.create_all()


# 홈페이지 렌더링
@app.route('/')
@app.route('/index',methods=['GET','POST'])
def home():
    return render_template('index.html')  # templates 폴더의 index.html 파일 렌더링


if __name__ == '__main__':
    app.run(debug=True)
