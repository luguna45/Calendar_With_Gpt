import olefile
import os
f = olefile.OleFileIO('test.hwp')  # olefile로 한글파일 열기
encoded_text = f.openstream('PrvText').read() # PrvText 스트림 안의 내용 꺼내기 (유니코드 인코딩 되어있음)
decoded_text = encoded_text.decode('utf-16')  # 유니코드이므로 utf-16으로 디코딩
print(decoded_text)