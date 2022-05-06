from cgitb import reset
from turtle import title
from flask import *  # Flask, render_template, request, send_file,Blueprint
import detect_plate
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io

from importlib import import_module

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pic.html', title="Image Rec.")


@app.route('/about')
def abt():
    return render_template('about.html', title="About")


@app.route('/excute', methods=['GET', 'POST'])
def exc():
    f = request.files['image']
    img = Image.open(f)
    result, data = detect_plate.Detect_Plate(img, True)
    json_object = json.dumps(data, ensure_ascii=True)
    with open("./sample.json", "w") as outfile:
        outfile.write(json_object)

    def serve_pil_image(pil_img):
        img_io = io.BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    fm = serve_pil_image(result)
    return fm


@app.route('/getPicData', methods=['GET', 'POST'])
def GetDat():
    f = open('./sample.json')
    jso = json.load(f)
    return jsonify(jso)  # "resp"


@app.route('/video', methods=['GET', 'POST'])
def videoMainPage():
    if request.method == 'POST':
        ip = request.form['ip']
        ips = "/video_feed?ip=" + ip  # "," + str(ip)
        global reset
        reset = False
        return render_template('video.html',title="Video Rec.", on=True, ips=ips , ip = ip)
    else:
        reset = True
        return render_template('video.html',title="Video Rec.", on=False, ips="", ip="")


@app.route('/video_feed')
def video_feed():
    ip = request.args.get('ip')

    return Response(gen(Camera(ip) ),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    return render_template('video.html', title="Video Rec.")


def gen(camera):

    yield b'--frame\r\n'

    while True:

        if(reset):
            return        


        frame = camera.get_frame()

        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


app.run(host='0.0.0.0', port=81, debug=True)
