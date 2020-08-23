from flask import Flask, request, redirect, url_for, render_template, flash, session
import requests
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET"])
def index():
    return render_template("top.html")

@app.route("/input", methods=["GET","POST"])
def input():
    if request.form["inputText"]:
        result = fetch()
        return render_template("result.html", data=result)
    else:
        flash("テキストが入力されていません")
        return render_template("top.html")

def fetch():
  #COTOHA APIのアクセストークンを取得する
  headers = {
      'Content-Type': 'application/json',
      'charset': 'UTF-8',
  }

  data = {
  "grantType":"client_credentials",
  "clientId":"example",
  "clientSecret":"example"
  }

  data = json.dumps(data).encode()
  response = requests.post('https://api.ce-cotoha.com/v1/oauth/accesstokens', headers=headers, data=data)
  access_token = response.json()['access_token']

  #属性推定APIを叩く
  URL_Endpoint = "https://api.ce-cotoha.com/api/dev/nlp/beta/user_attribute"
  headers = {
      'Content-Type': 'application/json',
      'charset': 'UTF-8',
      'Authorization': 'Bearer ' + access_token
  }
  
  data = {
  "document": request.form["inputText"],
  "type": "default"
  }

  data = json.dumps(data).encode()
  r = requests.post(URL_Endpoint, headers=headers, data=data)
  data = r.json()
  return data

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True) 
