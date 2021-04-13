# .\environment\Scripts\activate

from flask import Flask, render_template, Response,request,jsonify, redirect, url_for
import cv2
from photoDetection import *
import logging
from logger import createLog


createLog('user')
user = logging.getLogger('user')


app = Flask('templates')

#Initializing camera to capture video
camera = cv2.VideoCapture(0)

#Function which generates frames from the video and yeild it to render it live on html
def gen_frames():  
    while True:
        try:
            success, frame = camera.read()
            #processing frames for detection
            coords,out_frame,id_cropped_resized = imageCapture(frame,2)
        except cv2.error:
            user.error('Camera permissions not enabled')
            break
        else:            
            ret, buffer = cv2.imencode('.jpg', out_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/failed')
def failed():
    print("fail called")
    return render_template('fail.html')

@app.route('/idfailed')
def idfailed():
    print("id fail called")
    return render_template('idfail.html')

@app.route('/success')
def success():
    print("success called")
    return render_template('success.html')
  
# To capture image when verify button is clicked
@app.route('/capture_image', methods = ['POST'])
def capture_image():
    print("image captured")
    _, frame = camera.read()
    coords,out_frame,id_cropped_resized = imageCapture(frame,3)
    cv2.imwrite('image.jpg', out_frame)
    cv2.imwrite('id.jpg', id_cropped_resized)

    try:
        #verification of captured image
        result = verification(coords)
    except IndexError:
        print('two faces not identified')
        return "http://127.0.0.1:5000/failed"

    if(result=="VerificationSuccess"):
        print("verified")
        return "http://127.0.0.1:5000/success"

    elif(result=="FaceVerificationFailed"):
        return "http://127.0.0.1:5000/failed"
    
    elif(result=="IdVerificationFailed"):
        return "http://127.0.0.1:5000/idfailed"

# display video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)
