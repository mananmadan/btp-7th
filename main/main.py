from multiprocessing import Manager
from multiprocessing import Process
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
import config


# define the range for the motors
servoRange = (-90, 90)
cp = 0.0
ct = 0.0
son=False
        
def updateson():
    global son
    son = True
def getson():
    return son
# function to handle keyboard interrupt
def signal_handler(sig, frame):
	# print a status message
	print("[INFO] You pressed `ctrl + c`! Exiting...")
	# disable the servos
	pth.servo_enable(1, False)
	pth.servo_enable(2, False)
	# exit
	sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
	# signal trap to handle keyboard interrupt
	#global son
	signal.signal(signal.SIGINT, signal_handler)
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
				centerX.value = W // 2
				centerY.value = H // 2
				config.top = True
				
				updateson()
				print("temp toooop",config.top,getson())
				
				(x, y, w, h) = [int(v) for v in box]
				(objX.value,objY.value) = (int(x + (w / 2.0)), int(y + (h / 2.0)))
				cv2.circle(frame,(x+int(w/2),y+int(h/2)),2,(0,0,255),1)
				cv2.rectangle(frame, (x, y), (x + w, y + h),
					(0, 255, 0), 2)
				#print(y+h/2)
				
				
				
				
				#time.sleep( 1 )
		'''
			# update the FPS counter
			#fps.update()
			#fps.stop()

			# initialize the set of information we'll be displaying on
			# the frame
			
			info = [
				("Tracker", tr),
				("Success", "Yes" if success else "No"),
				("FPS", "{:.2f}".format(fps.fps())),
			]

			# loop over the info tuples and draw them on our frame
			for (i, (k, v)) in enumerate(info):
				text = "{}: {}".format(k, v)
				cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			
		'''

		# show the output frame
		#print("objX.value::::",objX.value)
		#print(objY.value)
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
			#top=True
			#son=True
			
			

			#fps = FPS().start()

		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break
		#print("here2")

	# if we are using a webcam, release the pointer
	#if not args.get("video", False):
	#vs.stop()
	cv2.destroyAllWindows()

def pid_process(output, p, i, d, objCoord, centerCoord):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)
	# create a PID and initialize it
	p = PID(p.value, i.value, d.value)
	p.initialize()
	# loop indefinitely
	while True:
		# calculate the error
		error = centerCoord.value - objCoord.value
		# update the value
		output.value = p.update(error)

def in_range(val, start, end):
	# determine the input value is in the supplied range
	return (val >= start and val <= end)
def set_servos(pan, tlt):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)
	global cp,ct
	# loop indefinitely
	while True:
		# the pan and tilt angles are reversed
		#print("pan-val",pan.value)
		#print("tilt-val",tlt.value)
		panAngle = +1 * pan.value
		tiltAngle = +1 * tlt.value
		# if the pan angle is within the range, pan
		# if in_range(panAngle, servoRange[0], servoRange[1]):
		#print("tilt",tiltAngle)
		print("Temp tooop 2",config.top,getson())
		cp = pth.pan(panAngle,cp,config.top)
		# if the tilt angle is within the range, tilt
		# if in_range(tiltAngle, servoRange[0], servoRange[1]):
		ct = pth.tilt(tiltAngle,ct,config.top)
		
    # check to see if this is the main body of execution
if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--cascade", type=str, required=True,
		help="path to input Haar cascade for face detection")
	args = vars(ap.parse_args())
    # start a manager for managing process-safe variables
	with Manager() as manager:
		# enable the servos
		pth.servo_enable(1, True)
		pth.servo_enable(2, True)
		# set integer values for the object center (x, y)-coordinates
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)
		# set integer values for the object's (x, y)-coordinates
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)
		# pan and tilt values will be managed by independed PIDs
		pan = manager.Value("i", 0)
		tlt = manager.Value("i", 0)
        # set PID values for panning
		panP = manager.Value("f", 0.09)
		panI = manager.Value("f", 0.08)
		panD = manager.Value("f", 0.002)
		# set PID values for tilting
		tiltP = manager.Value("f", 0.11)
		tiltI = manager.Value("f", 0.10)
		tiltD = manager.Value("f", 0.002)

        # we have 4 independent processes
		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center
		processObjectCenter = Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY))
		processPanning = Process(target=pid_process,
			args=(pan, panP, panI, panD, objX, centerX))
		processTilting = Process(target=pid_process,
			args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
		processSetServos = Process(target=set_servos, args=(pan, tlt))
		# start all 4 processes
		print("starting process")
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