from flask import Flask, render_template, Response
from webcamvideostream import WebcamVideoStream  # Import the updated class
import cv2
import time
app = Flask(__name__)
#123213
@app.route('/')
def index():
    return render_template('index.html')

def gen():
    camera = WebcamVideoStream(src=0, width=640, height=480).start()  # Singleton instance
    while True:
        frame = camera.read()
        if frame is None:
            print("No frame captured, stopping.")
            break
        ret, jpeg = cv2.imencode('.jpg', frame,  [cv2.IMWRITE_JPEG_QUALITY, 10])
        if jpeg is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            print("Frame is None, stopping.")
            break
        time.sleep(0.01)
        
    camera.stop()  # Stop and release the camera when done

@app.route('/camera')
def camera():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
