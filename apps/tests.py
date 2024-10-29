from flask import Flask

app = Flask(__name__)

@app.before_first_request
def create_tables():
    print("첫 번째 요청 전에 실행됩니다.")

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
