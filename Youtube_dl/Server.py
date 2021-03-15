from flask import Flask,render_template, request, redirect, url_for,session, flash
import os
from datetime import timedelta
import Youtube

app = Flask(__name__)
app.secret_key = "pewpew"
app.permanent_session_lifetime=timedelta(minutes=5)
dict = {}
prelinks ={}
links={}
dl=False
@app.route('/')
def home():
    global dl
    dl =False
    return render_template("index.html")


@app.route("/Download",methods=["POST","GET"])
def enter_link():
    global dl
    dl=False
    if request.method == "POST":
        session.permanent =True
        ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        pew = request.form["ui"]
        if "youtube" in pew or "youtu.be" in pew or "https" in pew:
            print(pew)
            videos=Youtube.Streams(pew)
            for ui in videos.keys():
                if ui != "img":
                    if videos[ui].resolution != None:
                        dict[ui]=videos[ui]
            dict["mp3"]=videos["mp3"]
            dict["img"]=videos["img"]
            dl=True
            if ip not in prelinks.keys():
                prelinks[ip]={}
            return redirect(url_for("encour"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/Choose",methods=["POST","GET"])
def encour():
    global dl
    if dl != False:
        ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if request.method == "POST":
            a=request.form.get("hey")
            Youtube.download(dict,a,prelinks[ip])
            return redirect(url_for("linked"))
        else:
            return render_template("encour.html",streams=dict)
    else:
        dl=False
        return render_template("index.html")

@app.route("/linked")
def linked():
    global dl
    dl=False
    ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if ip in prelinks:
        print(prelinks[ip])
        return render_template("linked.html",links=prelinks[ip])
    else:
        return render_template("linked.html",links=links)




if __name__ == "__main__":
    app.run(host='192.168.0.31')