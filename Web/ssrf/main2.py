# pip3 install flask
# python main.py

from flask import Flask, request, session
import requests
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(32)
INTERNAL_API = "http://127.0.0.1:8000/"
header = {"Content-Type": "application/x-www-form-urlencoded"}


@app.route("/v1/api/board/write", methods=["POST"])
def board_write():
    session["idx"] = "guest" # session idx를 guest로 설정합니다.
    title = request.form.get("title", "") # title 값을 form 데이터에서 가져옵니다.
    body = request.form.get("body", "") # body 값을 form 데이터에서 가져옵니다.
    data = f"title={title}&body={body}&user={session['idx']}" # 전송할 데이터를 구성합니다.
    response = requests.post(f"{INTERNAL_API}/board/write", headers=header, data=data) # INTERNAL API 에 이용자가 입력한 값을 HTTP BODY 데이터로 사용해서 요청합니다.
    return response.content # INTERNAL API 의 응답 결과를 반환합니다.
    
    
@app.route("/board/write", methods=["POST"])
def internal_board_write():
    # form 데이터로 입력받은 값을 JSON 형식으로 반환합니다.
    title = request.form.get("title", "")
    body = request.form.get("body", "")
    user = request.form.get("user", "")
    info = {
        "title": title,
        "body": body,
        "user": user,
    }
    return info
    
    
@app.route("/")
def index():
    # board_write 기능을 호출하기 위한 페이지입니다.
    return """
        <form action="/v1/api/board/write" method="POST">
            <input type="text" placeholder="title" name="title"/><br/>
            <input type="text" placeholder="body" name="body"/><br/>
            <input type="submit"/>
        </form>
    """
    
    
app.run(host="127.0.0.1", port=8000, debug=True)