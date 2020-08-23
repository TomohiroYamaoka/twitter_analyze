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
        return render_template("result.html",data1=result[0],data2=result[1],data3=result[2],data4=result[3],data5=result[4],data6=result[5])
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
  
  try: 
      data1=data['result']['age']
  except KeyError:
      data1="なし"   
  try: 
      data2=data['result']['civilstatus']
  except KeyError:
      data2="なし"
  try: 
      data3=data['result']['hobby']
  except KeyError:
      data3="なし"
  try: 
      data4=data['result']['occupation']
  except KeyError:
      data4="なし"
  try: 
      data5=data['result']['gender']
  except KeyError:
      data5="なし" 
  try: 
      data6=data['result']['moving']
  except KeyError:
      data6="なし"                             
  
  return data1,data2,data3,data4,data5,data6  

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True) 
