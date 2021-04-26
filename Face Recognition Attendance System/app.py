from flask import Flask, render_template, request, redirect
from PIL import Image
import cv2
import numpy as np
import face_recognition
import base64
import io
import os
from utils import *


app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="")

# routes
@app.route("/")
def home_page():
    return render_template("templates/home.html")

@app.route("/enroll", methods=['GET', 'POST'])
def kuch_bhi():
    return render_template("templates/enrollment.html")

@app.route("/remove_face", methods=['GET', 'POST'])
def kuch_bhi_nhi():
    return render_template("templates/remove.html")

@app.route("/run_attendance_server")
def run_attendance_server():
    os.system("python mark_attendance.py")
    return redirect("/", code=302)

@app.route("/view_report")
def view_report():
    return render_template("Report.html")

@app.route("/remove", methods = ['GET', 'POST'])
def remove():
    if request.method == 'POST':
        msg = ""
        form_data = dict(request.form)
        ID = form_data['student_id']
        name, img_path, msg = remove_face(ID)
        return render_template("templates/remove.html", res = ID, img_path = img_path, name = name, msg = msg)


@app.route("/submit", methods = ['GET', 'POST'])
def face_enroll():
    if request.method == 'POST':
        msg = ""
        img = request.files['my_image']
        image_string = base64.b64encode(img.read())
        image_string = image_string.decode('utf-8')
        image = stringToRGB(image_string)
        #img_path = "static/" + img.filename
        form_data = dict(request.form)
        name = form_data['student_name']
        ID = form_data['student_id']
        msg = enroll_face(name, ID, image)
        img_path = "static/enrolled/" + ID + ".jpg"
        #img.save(img_path)
        cv2.imwrite(img_path, image)
        return render_template("templates/enrollment.html", res = ID, img_path = img_path, name = name, msg = msg)


if __name__ =='__main__':
    #app.debug = True
    app.run("0.0.0.0", 5000, threaded=False, debug=False)