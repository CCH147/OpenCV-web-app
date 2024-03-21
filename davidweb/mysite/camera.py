import imutils
import urllib
from imutils.video import VideoStream
import cv2
import os
import requests
import numpy as np
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'davidweb.settings')


face_detection = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'face detector/haarcascade_frontalface_alt2.xml'))

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces_detected = face_detection.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)
		for (x, y, w, h) in faces_detected:
			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()

