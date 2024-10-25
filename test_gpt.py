from openai import OpenAI

c=OpenAI(api_key="chatgpt key")




response = c.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": '''
                받은 입력에서 날짜와 시간정보를 분류하고 일정내용을 간단하고 명확하게 요약후 출력 형식에 맟춰 출력
                출력형식: 날짜:yyyy-mm-dd,시간:hh:mm-hh:mm또는 x (시간정보없을때),일정: 간단한 일정설명
                '''},
                {"role": "user", "content": "2024년 4월 19일 입학식 있으니 늦지 않도록"}
            ])

response_content = response.choices[0].message.content
print(response_content)