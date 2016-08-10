#!/usr/bin/python

import cv2
from bottle import request, response, route, run

WRAPPER_HTML = """
<html>
  <header></header>
  <body>
    <img id="frontImage">
    <img id="backImage" style="display: none;">

    <script>
      (function() {
      var frontImage = document.getElementById("frontImage");
      var backImage = document.getElementById("backImage");
      var frameNum = 0;
      var id = Math.floor(Math.random() * 99999);
      function requestNext() {
        frameNum = frameNum + 1;
        backImage.src = "frame.jpg?f=" + frameNum + "&id=" + id;
      };
      backImage.addEventListener("load", function() {
        frontImage.src = backImage.src;
        requestNext();
      });
      requestNext();
      })();
    </script>
  </body>
</html>
"""

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

shown = None
jpg_raw = None

def get_jpg(id, clientip):
    global shown
    global jpg_raw
    key = (id, clientip)
    if not jpg_raw or key in shown:
        shown = set( )
        _, frame = cap.read()
        _, jpg = cv2.imencode('.jpg', frame)
        jpg_raw = jpg.tostring()
    shown.add(key)
    return jpg_raw

@route('/frame.jpg')
def stream():
    params = request.query.decode()
    clientip = request.environ.get('REMOTE_ADDR')
    response.set_header('Content-Type', 'image/jpeg')
    return get_jpg(params.get('id', 0), clientip)

@route('/')
def wrapper():
    return WRAPPER_HTML

run(host='0.0.0.0', port=8081, quiet=True)
