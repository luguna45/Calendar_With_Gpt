from flask import Flask, jsonify, render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from pyFile.Parsing import Parsings
from pyFile.web_crawler import crawling
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
    

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(6), nullable=False)
    # start=db.Column(db.DateTime, nullable=False) 
    end = db.Column(db.String(100), nullable=True)
    # end = db.Column(db.DateTime, nullable=True)
    def to_dict(self):
        return {
            "title": self.title,
            "start": self.start,
            "end": self.end if self.end else None,
        }
#모든 이벤트 가져오기
@app.route('/events', methods=['GET'])
# @login_required
def get_events():
    # events = Event.query.filter_by(user_id=current_user.id).all()
    events = Event.query.all()  # 모든 이벤트 쿼리
    return jsonify([event.to_dict() for event in events])

@app.route('/events', methods=['POST'])
# @login_required
def add_event():
    data = request.json
    new_event = Event(
        title=data['title'],
        start=data['start'],
        end=data['end'] if data.get('end') else None,
        # user_id=current_user.id
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201  # 저장 후 이벤트 반환




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


@app.route('/parsing')
def webparsing():
    with app.app_context():
        # class Event(db.Model):
        #     __tablename__ = 'events'
        #     id = db.Column(db.Integer, primary_key=True)
        #     title = db.Column(db.String(100), nullable=False)
        #     start = db.Column(db.String(6), nullable=False)
        #     # start=db.Column(db.DateTime, nullable=False) 
        #     end = db.Column(db.String(100), nullable=True)
        #     # end = db.Column(db.DateTime, nullable=True)
        #     def to_dict(self):
        #         return {
        #             "title": self.title,
        #             "start": self.start,
        #             "end": self.end if self.end else None,
        #         }

        for event in Parsings():
            event_str = event[0]
            parts = event_str.split(', ')
            # print(parts)
            start_date = parts[0].split(',')[0].split('/')[1]
            end_date =   parts[0].split(',')[1].split('/')[1]
            title= parts[0].split(',')[2].split('/')[1]
            # print(end_date)  # 시작 날짜 추출
            # Event 객체 생성
            new_event = Event(title=title, start=start_date, end=end_date)
            print(new_event)
            # 세션에 추가
            db.session.add(new_event)

        # 변경사항 저장
        db.session.commit()



# 홈페이지 렌더링
@app.route('/')
@app.route('/index',methods=['GET','POST'])
def home():
    return render_template('index.html')  # templates 폴더의 index.html 파일 렌더링


if __name__ == '__main__':
    app.run(debug=True)
