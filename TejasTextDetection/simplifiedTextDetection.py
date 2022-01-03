import numpy as np
import cv2 as cv
import math
import time
import os,sys



def fourPointsTransform(frame, vertices):
	vertices = np.asarray(vertices)
	outputSize = (100, 32)
	targetVertices = np.array([
		[0, outputSize[1] - 1],
		[0, 0],
		[outputSize[0] - 1, 0],
		[outputSize[0] - 1, outputSize[1] - 1]], dtype="float32")

	rotationMatrix = cv.getPerspectiveTransform(vertices, targetVertices)
	result = cv.warpPerspective(frame, rotationMatrix, outputSize)
	return result

def decodeText(scores):
	text = ""
	alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
	for i in range(scores.shape[0]):
		c = np.argmax(scores[i][0])
		if c != 0:
			text += alphabet[c - 1]
		else:
			text += '-'

	# adjacent same letters as well as background text must be removed to get the final output
	char_list = []
	for i in range(len(text)):
		if text[i] != '-' and (not (i > 0 and text[i] == text[i - 1])):
			char_list.append(text[i])
	return ''.join(char_list)


def decodeBoundingBoxes(scores, geometry, scoreThresh):
	detections = []
	confidences = []

	############ CHECK DIMENSIONS AND SHAPES OF geometry AND scores ############
	assert len(scores.shape) == 4, "Incorrect dimensions of scores"
	assert len(geometry.shape) == 4, "Incorrect dimensions of geometry"
	assert scores.shape[0] == 1, "Invalid dimensions of scores"
	assert geometry.shape[0] == 1, "Invalid dimensions of geometry"
	assert scores.shape[1] == 1, "Invalid dimensions of scores"
	assert geometry.shape[1] == 5, "Invalid dimensions of geometry"
	assert scores.shape[2] == geometry.shape[2], "Invalid dimensions of scores and geometry"
	assert scores.shape[3] == geometry.shape[3], "Invalid dimensions of scores and geometry"
	height = scores.shape[2]
	width = scores.shape[3]
	for y in range(0, height):

		# Extract data from scores
		scoresData = scores[0][0][y]
		x0_data = geometry[0][0][y]
		x1_data = geometry[0][1][y]
		x2_data = geometry[0][2][y]
		x3_data = geometry[0][3][y]
		anglesData = geometry[0][4][y]
		for x in range(0, width):
			score = scoresData[x]

			# If score is lower than threshold score, move to next x
			if (score < scoreThresh):
				continue

			# Calculate offset
			offsetX = x * 4.0
			offsetY = y * 4.0
			angle = anglesData[x]

			# Calculate cos and sin of angle
			cosA = math.cos(angle)
			sinA = math.sin(angle)
			h = x0_data[x] + x2_data[x]
			w = x1_data[x] + x3_data[x]

			# Calculate offset
			offset = ([offsetX + cosA * x1_data[x] + sinA * x2_data[x], offsetY - sinA * x1_data[x] + cosA * x2_data[x]])

			# Find points for rectangle
			p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
			p3 = (-cosA * w + offset[0], sinA * w + offset[1])
			center = (0.5 * (p1[0] + p3[0]), 0.5 * (p1[1] + p3[1]))
			detections.append((center, (w, h), -1 * angle * 180.0 / math.pi))
			confidences.append(float(score))

	# Return detections and confidences
	return [detections, confidences]




def get_words(image_path,detector,recognizer,nms_thresh=0.4,confidence_thresh=0.5,resize_width=320,resize_height=320):
	
	confThreshold = confidence_thresh
	nmsThreshold = nms_thresh
	inpWidth = resize_width
	inpHeight = resize_height
	
	bounding_boxes={}
	
	
	outNames = []
	outNames.append("feature_fusion/Conv_7/Sigmoid")
	outNames.append("feature_fusion/concat_3")

	frame=cv.imread(image_path)
	cv.imshow('image',frame)
	
	height_ = frame.shape[0]
	width_ = frame.shape[1]
	rW = width_ / float(inpWidth)
	rH = height_ / float(inpHeight)

	blob = cv.dnn.blobFromImage(frame, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

	detector.setInput(blob)
	outs = detector.forward(outNames)

	scores = outs[0]
	geometry = outs[1]
	[boxes, confidences] = decodeBoundingBoxes(scores, geometry, confThreshold)

	indices = cv.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)

	for i in indices:
			# get 4 corners of the rotated rect
			vertices = cv.boxPoints(boxes[i])
			# scale the bounding box coordinates based on the respective ratios
			for j in range(4):
				vertices[j][0] *= rW
				vertices[j][1] *= rH
			
			if True:
				cropped = fourPointsTransform(frame, vertices)
				cropped = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
				
				#bottom left
				x1=int(vertices[0][0])
				y1=int(vertices[0][1])
				#top left
				x2=int(vertices[1][0])
				y2=int(vertices[1][1])
				#top right
				x3=int(vertices[2][0])
				y3=int(vertices[2][1])
				#bottom right
				x4=int(vertices[3][0])
				y4=int(vertices[3][1])
				
				

				# Create a 4D blob from cropped image
				blob = cv.dnn.blobFromImage(cropped, size=(100, 32), mean=127.5, scalefactor=1 / 127.5)
				recognizer.setInput(blob)
				#run model
				result = recognizer.forward()
				wordRecognized = decodeText(result)
				
				bounding_boxes[(x1,y1)]=wordRecognized
				
				
				#print(f"recognized word is {wordRecognized} vertices={[x1,y1],[x2,y2]}, confidence={int(confidences[i]*100)}")
	return sort_points(list(bounding_boxes.keys()),bounding_boxes)

def sort_points(keypoints,dicta):
	points = []
	keypoints_to_search = keypoints[:]
	while len(keypoints_to_search) > 0:
		a = sorted(keypoints_to_search, key=lambda p: (p[0]) + (p[1]))[0]  # find upper left point
		b = sorted(keypoints_to_search, key=lambda p: (p[0]) - (p[1]))[-1]  # find upper right point

		

		# convert opencv keypoint to numpy 3d point
		a = np.array([a[0], a[1], 0])
		b = np.array([b[0], b[1], 0])

		row_points = []
		remaining_points = []
		for k in keypoints_to_search:
			p = np.array([k[0], k[1], 0])
			d = len(k)  # diameter of the keypoint (might be a theshold)
			dist = np.linalg.norm(np.cross(np.subtract(p, a), np.subtract(b, a))) / np.linalg.norm(b)   # distance between keypoint and line a->b
			if d/2 > dist:
				row_points.append(k)
			else:
				remaining_points.append(k)

		points.extend(sorted(row_points, key=lambda h: h[0]))
		keypoints_to_search = remaining_points
	
	return points,dicta
		

def main():
	
	image_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/camera_image.jpeg";
	text_detection_model_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/frozen_east_text_detection.pb";
	text_recognition_model_path="/home/pi/Desktop/GitHub/OurVision/TejasTextDetection/crnn.onnx";
	
	print("loading models please wait......")
	
	detector_model = cv.dnn.readNet(text_detection_model_path)
	recognizer_model = cv.dnn.readNet(text_recognition_model_path)
	
	print("models loaded")
	
	
	
	#i=int(input("enter 1 to continue "));
	i=1
	if (i==1):
        
		start = time.time()
		#os.popen('libcamera-jpeg -o camera_image.jpeg -t 5000 ')
		ordr_points,dicta=get_words(image_path,detector_model,recognizer_model,nms_thresh=0.4,confidence_thresh=0.5,resize_width=320,resize_height=320)
		#sort_points(list(bounding_boxes.keys()))
		for i in ordr_points:
			print(dicta[i])
			
		print(time.time() - start)
main()
    

