from flask import Flask, render_template, request, send_file,Response
import detect_plate
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np
import io
from io import StringIO ,BytesIO
import base64
app = Flask(__name__)


@app.route('/')
def index():
    #data = detect_plate.Detect_Plate()
    # str(data) #'Web App with Python Flask!'
    return render_template('index.html')


@app.route('/excute', methods=['GET', 'POST'])
def exc():
    print(request.files)
    f = request.files['image']
    img = Image.open(f)
    result = detect_plate.Detect_Plate(img)
    print(result)
    print(type(result))
    # Image.save(result)

    def serve_pil_image(pil_img):
        img_io = io.BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    

    def stream_template(template_name, **context):
        app.update_template_context(context)
        t = app.jinja_env.get_template(template_name)
        rv = t.stream(context)
        rv.enable_buffering(5)
        return rv
    # q = result.save(os.path.join('/', 'temp.jpg'))
    # return render_template('result.html' , mg = q)

    fm = serve_pil_image(result)
    # return Response(stream_template('result.html', img=fm))
    return fm
    return str(result)
   # return send_file(result, mimetype='image')#result#send_file(os.path.abspath(secure_filename(result.filename)), mimetype='image/gif') #render_template('result.html', image=os.path.abspath(secure_filename(f.filename)))#str(result) #request.files['profile_pic'] #render_template('index.html')#str(data) #'Web App with Python Flask!'


@app.route('/my-large-page.html')
def render_large_template():
    rows = iter_all_rows()
    return Response(stream_template('the_template.html', img=fm))

app.run(host='0.0.0.0', port=81, debug=True)

