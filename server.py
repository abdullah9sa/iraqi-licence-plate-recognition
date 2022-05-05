from turtle import title
from flask import *#Flask, render_template, request, send_file,Blueprint
import detect_plate
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np
import io
from io import StringIO ,BytesIO
import base64
from flask import jsonify
app = Flask(__name__)
#import json 

@app.route('/')
def index():
    #data = detect_plate.Detect_Plate()
    # str(data) #'Web App with Python Flask!'
    return render_template('pic.html' , title = "Image Rec.")

@app.route('/video')
def vid():
    #data = detect_plate.Detect_Plate()
    # str(data) #'Web App with Python Flask!'
    return render_template('video.html', title = "Video Rec.")

@app.route('/about')
def abt():
    #data = detect_plate.Detect_Plate()
    # str(data) #'Web App with Python Flask!'
    return render_template('about.html', title = "About")


@app.route('/excute', methods=['GET', 'POST'])
def exc():
    f = request.files['image']
    img = Image.open(f)
    result,data = detect_plate.Detect_Plate(img)
    print("-----------------")
    print(data)
    print("-----------------")
    json_object = json.dumps(data,ensure_ascii = True)
    # json_object = jsonify(data)
    with open("./sample.json", "w") as outfile:
        outfile.write(json_object)


    def serve_pil_image(pil_img):
        img_io = io.BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    # buffered = BytesIO()
    # result.save(buffered, format="JPEG")
    # img_str = base64.b64encode(buffered.getvalue())


    fm = serve_pil_image(result)
    # # print(img_str)
    # jsony = jsonify(
    #     imageData = str(img_str),#str(img_str),
    #     num = "123",
    #     city = "baghdad",
    #     state = "Chicago"
    # )
    # print(img_str)
    # fm = serve_pil_image(result)
    return fm

@app.route('/getPicData', methods=['GET', 'POST'])
def GetDat():
    # print(globalData)
    # resp = jsonify(globalData)
    f = open('./sample.json')
    jso = json.load(f)
    return jsonify(jso)#"resp"



app.run(host='0.0.0.0', port=81, debug=True)

