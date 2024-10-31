from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
app=Flask(__name__)

a=[['시작날짜/2024-10-08T00:00:00,종료날짜/2024-10-14T00:05:00,일정/도제준비 신청'], 
 ['시작날짜/2024-11-01T00:00:00,종료날짜/2024-11-29T00:05:00,일정/11월 급식기간'], 
 ['시작날짜/2024-10-21T00:00:00,종료날짜/2024-10-24T00:05:00,일정/국어과목선택 수요조사'], 
 ['시작날짜/2024-10-21T00:00:00,종료날짜/2024-10-24T00:05:00,일정/교과선택 1차 수요조사'], 
 ['시작날짜/2024-10-18,종료날짜/2024-10-18,일정/소규모 교육여행 참여 여부 조사 결과 안내'], 
 ['시작날짜/2024-10-07T00:00:00,종료날짜/2024-10-11T00:05:00,일정/교육여행 수요조사'], 
 ['시작날짜/2024-11-04T10:40:00,종료날짜/2024-11-04T15:00:00,일정/생존수영 교육'], 
 ['시작날짜/2024-10-7T16:20:00,종료날짜/2024-10-14T19:10:00,일정/자율학습신청', ''], 
 ['시작날짜/2024-10-30T08:20:00,종료날짜/2024-10-30T11:45:00,일정/학교혁신 한마당'], 
 ['시작날짜/2024-10-18T09:10:00,종료날짜/2024-10-18T12:10:00,일정/도제학교 취업박람회']]

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # 데이터베이스 URI 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#24비트 랜덤 바이트 비밀키
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)
with app.app_context():
    # 기존 테이블 삭제 (필요한 경우)
    db.drop_all()
    # 데이터베이스 테이블 생성
    db.create_all()
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

    for event in a:
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
