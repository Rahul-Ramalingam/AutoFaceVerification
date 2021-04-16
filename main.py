# .\environment\Scripts\activate

from flask import Flask, render_template, Response,request,jsonify, redirect, url_for
import cv2
from photoDetection import UserVerification
from util import loadIds
import logging
from logger import createLog


createLog('user')
user = logging.getLogger('user')



app = Flask('templates')

#Initializing camera to capture video
camera = cv2.VideoCapture(0)
images = loadIds()

#object created for user verification task 
#this class expects the original ID images 
verify = UserVerification(images)

#Function which generates frames from the video and yeild it to render it live on html
def gen_frames():  
    while True:
        try:
            success, frame = camera.read()
            #processing frames for detection
            coords,out_frame,id_cropped_resized =  verify.imageCapture(frame,2)
        except cv2.error:
            user.error("camera not open")
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
    user.info("face verification fail")
    return render_template('fail.html')

@app.route('/idfailed')
def idfailed():
    user.info("id verification fail")
    return render_template('idfail.html')

@app.route('/success')
def success():
    user.info("success called")
    return render_template('success.html')
  
# this function is called when user clicks the verify button
@app.route('/capture_image', methods = ['POST'])
def capture_image():
    print("image captured")
    _, frame = camera.read()
    coords,out_frame,id_cropped_resized = verify.imageCapture(frame,3)
    cv2.imwrite('image.jpg', out_frame)
    cv2.imwrite('id.jpg', id_cropped_resized)

    try:
        #verify the captured image
        result = verify.verification(coords)
    except IndexError:
        user.warning('two faces not identified')
        return "http://127.0.0.1:5000/failed"

    if(result=="VerificationSuccess"):
        user.info("verified")
        return "http://127.0.0.1:5000/success"

    elif(result=="FaceVerificationFailed"):
        return "http://127.0.0.1:5000/failed"
    
    elif(result=="IdVerificationFailed"):
        return "http://127.0.0.1:5000/idfailed"

# renders video feed to html
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)
