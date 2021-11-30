from imutils.video import VideoStream
from objcenter import ObjCenter
from pid import PID
import pantilthat as pth
import argparse
import signal
import time
import logging
import sys
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import threading
import os
from flask import Flask, render_template, Response, request


# define the range for the motors
servoRange = (-90, 90)
cp = 0.0
ct = 0.0

objX=0
objY=0
centerX=0
centerY=0
pan = 0
tlt = 0
panP = 2.0
panI = 0.0
panD = 0.7
tiltP =2.0
tiltI =0.0
tiltD = 0.7
tltError=0
top=False
img=[[[]]]
# function to handle keyboard interrupt
def signal_handler(sig, frame):
	# print a status message
	print("[INFO] You pressed `ctrl + c`! Exiting...")
	# disable the servos
	pth.servo_enable(1, False)
	pth.servo_enable(2, False)
	# exit
	os._exit(1)
	sys.exit()

def obj_center():
	# signal trap to handle keyboard interrupt
	#global son
	global objX, objY, centerX, centerY,top,img
	#signal.signal(signal.SIGINT, signal_handler)
	tracker = cv2.TrackerKCF_create()
	# initialize the bounding box coordinates of the object we are going
	# to track
	initBB = None
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	# initialize the FPS throughput estimator
	fps = None
	# loop over frames from the video stream
	while True:
		frame = vs.read()
		img=frame.copy()
		if frame is None:
			break
		# resize the frame (so we can process it faster) and grab the
		# frame dimensions
		frame = imutils.resize(frame, width=500)
		(H, W) = frame.shape[:2]
		
		
		# check to see if we are currently tracking an object
		
		if initBB is not None:
			# grab the new bounding box coordinates of the object
			(success, box) = tracker.update(frame)
			#print(success)
			# check to see if the tracking was a success
			if success:
				# find the object's location
				centerX = W // 2
				centerY = H // 2
				
				
				#print("temp toooop",config.top,getson())
				
				(x, y, w, h) = [int(v) for v in box]
				(objX,objY) = (int(x + (w / 2.0)), int(y + (h / 2.0)))
				cv2.circle(frame,(x+int(w/2),y+int(h/2)),2,(0,0,255),1)
				cv2.rectangle(frame, (x, y), (x + w, y + h),
					(0, 255, 0), 2)
				
				
		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if key == ord("s"):
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)
			initBB = cv2.selectROI("Frame", frame, fromCenter=False,
				showCrosshair=True)
			#print(initBB)
			# start OpenCV object tracker using the supplied bounding box
			# coordinates, then start the FPS throughput estimator as well
			tracker.init(frame, initBB)
			top=True
			#fps = FPS().start()
		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break
		
	# if we are using a webcam, release the pointer
	#if not args.get("video", False):
	#vs.stop()
	cv2.destroyAllWindows()

def pid_process_pan():
    
	# signal trap to handle keyboard interrupt
	#signal.signal(signal.SIGINT, signal_handler)
	# create a PID and initialize it
	global pan, objX, centerX,panP,panI,panD
	pi = PID(panP, panI, panD)
	pi.initialize()
	# loop indefinitely
	while True:
		# calculate the error
		error = centerX - objX
		if error < 35 and error > -35:
		  error = 0
		pan = pi.update(error)

def pid_process_tilt():
    
	# signal trap to handle keyboard interrupt
	global tlt, objY, centerY,tiltP,tiltI ,tiltD ,tltError
	#signal.signal(signal.SIGINT, signal_handler)
	# create a PID and initialize it
	pi = PID(tiltP, tiltI, tiltD)
	pi.initialize()
	# loop indefinitely
	while True:
		# calculate the error
		tltError = centerY - objY
		if tltError < 50 and tltError > -50:
		  tltError = 0
		print(centerY,objY,tltError)
		tlt = pi.update(tltError)

def in_range(val, start, end):
	# determine the input value is in the supplied range
	return (val >= start and val <= end)
def set_servos():
	# signal trap to handle keyboard interrupt
	#signal.signal(signal.SIGINT, signal_handler)
	global cp,ct,pan,tlt,tltError
	# loop indefinitely
	while True:
		# the pan and tilt angles are reversed
		panAngle = +1 * pan
		tiltAngle = +1 * tlt
		#print(pan,tlt)
		cp = pth.pan(panAngle,cp,top)
		ct = pth.tilt(tiltAngle,ct,tltError)
		
    # check to see if this is the main body of execution
app = Flask(__name__)
def gen_frames():  
    global img
    while True:
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # start a manager for managing process-safe variables
    # we have 4 independent processes
    # 1. objectCenter  - finds/localizes the object
    # 2. panning       - PID control loop determines panning angle
    # 3. tilting       - PID control loop determines tilting angle
    # 4. setServos     - drives the servos to proper angles based
    #                    on PID feedback to keep object in center
    
		pth.servo_enable(1, False)
		pth.servo_enable(2, False)
		signal.signal(signal.SIGINT, signal_handler)
		processObjectCenter = threading.Thread(target=obj_center)
		processPanning = threading.Thread(target=pid_process_pan)
		processTilting = threading.Thread(target=pid_process_tilt)
		processSetServos = threading.Thread(target=set_servos)
		# start all 4 processes
		print("starting process")
		threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)).start()
		processObjectCenter.start()
		print("Object center started")
		processPanning.start()
		print("Panning started")
		processTilting.start()
		print("Tilting started")
		processSetServos.start()
		print("joining")
		time.sleep(2)
		# join all 4 processes
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processSetServos.join()
		# disable the servos
		pth.servo_enable(1, False)
		pth.servo_enable(2, False)

