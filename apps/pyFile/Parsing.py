# from test_gpt import chatgptParsing
from openai import OpenAI
import olefile
import os
path=os.path.abspath("./hwpFile")
filelist=os.listdir(path)
turnChat=[]
def Parsings():
    for i in range(0,len(filelist),1):
        f = olefile.OleFileIO(os.path.join(path, filelist[i]))  # olefile로 한글파일 열기
        encoded_text = f.openstream('PrvText').read() # PrvText 스트림 안의 내용 꺼내기 (유니코드 인코딩 되어있음)
        # decoded_text=decoded_text+encoded_text.decode('utf-16')# 유니코드이므로 utf-16으로 디코딩
        decoded_text=encoded_text.decode('utf-16')# 유니코드이므로 utf-16으로 디코딩
        # print(decoded_text)
        # turnChat=turnChat+chatgptParsing(decoded_text)
        turnChat.append(chatgptParsing(decoded_text))
        print(i)

    # a= "2024년 4월 19일 입학식 있으니 늦지 않도록,2024년 5시 15분 10월 16일 무슨일이 있었을까 바로 학교가 쉬는날이였다 2024년 12월 30일부터 1월 10일까지 메이커스 체험이 있습니다"
    # print(chatgptParsing(a))
    print(turnChat)
    return turnChat

def chatgptParsing(intext):
    # intext="2024년 4월 19일 입학식 있으니 늦지 않도록,2024년 5시 15분 10월 16일 무슨일이 있었을까 바로 학교가 쉬는날이였다"
    
    c=OpenAI(api_key="key")


    response = c.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": '''
                    받은 입력에서 날짜와 시간정보를 분류하고 일정내용을 간단하고 명확하게 요약후 출력 형식에 맟춰 출력
                    일정의 시작,끝,일정 형식으로 출력한다 각 시작,끝,일정은,출력형식을 따른다
                    
                    출력형식: 날짜/yyyy-mm-dd,시간/hh:mm-hh:mm또는 x (시간정보없을때),일정/ 간단한 일정설명
                    일정의 시작과 끝은 서로 다른 키로 구분되어야한다
                    예로 '24년 12월 20일 12시 31분부터 21일 12시40분까지 건담 행사가 진행됨니다'일정은
                    '시작날짜/2024-12-20T12:31:00,종료날짜/2024-12-21T12:40:00,일정/건담행사'으로 한다
                    종료 날짜가 없을경우 시작날짜의 시간에 5분을 추가해서 종료날짜에 저장한다
                    시작날짜의 시간이 없다면 종료날짜와 시작날짜을 동일하게 저장한다
                    일정설명은 캘린더의 핵심만이용해 간단하게 요약해야한다
                    일정설명이 되도록 10글자 이상을 넘지 않도록 한다
                    일정설명은 년도나 시간 날짜를 되도록 언급하지 않는다
                    급식안내와 같이 활동이나 학교생활에 관련되지 않은것은 포함하지 않는다
                    무엇인가를 신청하는 기간이나 마감같은경우 다른 사족없이 핵심 목적만을 사용한다
                    예로 '2023년도 제 4기 학과체험 신청' 같은경우 학과체험 신청 으로 일정을 요약한다
                    일정은 무엇을 한다 혹은 확정사항만을 포함한다
                    
                    '''},
                    {"role": "user", "content": intext}
                ])
                        # 똑같은 시간/날짜/일정은 중복 출력하지 않고 하나만 출력한다
    #chatgpt 응답중 message 저장
    response_content = response.choices[0].message.content
    try:
        line=response_content.split('\n')
    except:
        line=[f'{response_content}']

    # for i in line:
    #     print(f'{i}\n')
    return line

# Parsings()

# [['시작날짜/2024-10-08T00:00:00,종료날짜/2024-10-14T00:05:00,일정/도제준비 신청'], 
#  ['시작날짜/2024-11-01T00:00:00,종료날짜/2024-11-29T00:05:00,일정/11월 급식기간'], 
#  ['시작날짜/2024-10-21T00:00:00,종료날짜/2024-10-24T00:05:00,일정/국어과목선택 수요조사'], 
#  ['시작날짜/2024-10-21T00:00:00,종료날짜/2024-10-24T00:05:00,일정/교과선택 1차 수요조사'], 
#  ['시작날짜/2024-10-18,종료날짜/2024-10-18,일정/소규모 교육여행 참여 여부 조사 결과 안내'], 
#  ['시작날짜/2024-10-07T00:00:00,종료날짜/2024-10-11T00:05:00,일정/교육여행 수요조사'], 
#  ['시작날짜/2024-11-04T10:40:00,종료날짜/2024-11-04T15:00:00,일정/생존수영 교육'], 
#  ['시작날짜/2024-10-7T16:20:00,종료날짜/2024-10-14T19:10:00,일정/자율학습신청', ''], 
#  ['시작날짜/2024-10-30T08:20:00,종료날짜/2024-10-30T11:45:00,일정/학교혁신 한마당'], 
#  ['시작날짜/2024-10-18T09:10:00,종료날짜/2024-10-18T12:10:00,일정/도제학교 취업박람회']]