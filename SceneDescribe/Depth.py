import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
from scipy import stats

import time

class SceneDescribe:
	def __init__(self,depth_model_path=None, object_detection_model_path=None):
		
		self.depth_model = tflite.Interpreter(model_path=depth_model_path ,num_threads=4)
		self.depth_model.allocate_tensors()
		
		self.object_detection_model = tflite.Interpreter(model_path=object_detection_model_path ,num_threads=4)
		self.object_detection_model.allocate_tensors()
		
		self.labels = {}
		#self.labels[0]='background'
		key=0
		with open("SceneDescribe/labelmap.txt") as f:
			for line in f:
				val=line
				self.labels[key] = val[:-1]
				key+=1
		
	
	def get_depth_map(self,image_array=None):

		#loading the image
		
		src = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

		# Load the TFLite model and allocate tensors.
		interpreter=self.depth_model

		# Get input and output tensors.
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()
		input_shape = input_details[0]['shape']

		input_data = cv2.resize(src,(256,256),interpolation=cv2.INTER_CUBIC)/255.0
		mean=[0.485, 0.456, 0.406]
		std=[0.229, 0.224, 0.225]
		input_data = (input_data - mean) / std
		input_data = input_data.reshape(1,256,256,3).astype('float32')
		interpreter.set_tensor(input_details[0]['index'], input_data)

		interpreter.invoke()

		# The function `get_tensor()` returns a copy of the tensor data.
		# Use `tensor()` in order to get a pointer to the tensor.
		output_data = interpreter.get_tensor(output_details[0]['index'])
		output_data = output_data.reshape(256,256)


		prediction = cv2.resize(output_data, (np.shape(image_array)[1],np.shape(image_array)[0]), interpolation=cv2.INTER_CUBIC)
		depth_min = prediction.min()
		depth_max = prediction.max()
		img_out = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")
		
		'''
		#print(img_out)
		cv2.imwrite("output.png", img_out)
		'''
		
		return(img_out)
	
	def get_object_bounding_boxes(self,image_array=None):
		
		resize_width=320
		resize_height=320
		
		src = image_array#cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
		
		interpreter=self.object_detection_model
		
		input_details = interpreter.get_input_details()
		#print(input_details)
		output_details = interpreter.get_output_details()
		input_shape = input_details[0]['shape']
		
		#print(f"input shape{input_shape}")
		# output indices are [601, 599, 598, 600], tensor names and indices aligned
		# are:
		#   - location: 598
		#   - category: 599
		#   - score: 600
		#   - detection_count: 601
		location_index=598
		category_index=599
		score_index=600
		detection_count_index=601
		
		input_data = cv2.resize(src,(resize_width,resize_height))
		mean=127.5
		std=127.5
		#input_data = (input_data - mean) / std
		#input_data = input_data.reshape(1,resize_width,resize_height,3).astype('uint8')
		input_data = np.expand_dims(input_data, axis=0)
		interpreter.set_tensor(input_details[0]['index'], input_data)
		
		interpreter.invoke()
		locations = interpreter.get_tensor(location_index)[0]
		categories= interpreter.get_tensor(category_index)[0]
		scores= interpreter.get_tensor(score_index)[0]
		detection_count = interpreter.get_tensor(detection_count_index)[0]
		
		

		resize_height1,resize_width1,t=np.shape(image_array)
		#print(resize_width1,resize_height1)
		for i in range(25):
			#break
			locations[i,0]=int(locations[i,0]*resize_height1) #left
			locations[i,1]=int(locations[i,1]*resize_width1) #top
			locations[i,2]=int(locations[i,2]*resize_height1) #right
			locations[i,3]=int(locations[i,3]*resize_width1)  #bottom
		
		#print(locations[0])
		final_data=[] #[label, score, position]
		for i in range(25):
			final_data.append([self.labels[categories[i]], scores[i] ,locations[i]])
		
		'''
		#image_array=cv2.imread('output.png')
		for i in range(5):
			img = cv2.rectangle(image_array, (int(locations[i,1]),int(locations[i,0])), (int(locations[i,3]),int(locations[i,2])),(255, 0, 0), 2)
		#print(categories)
		cv2.imwrite("output2.png", img)
		'''
		
		return final_data
	
	def describe(self,img):
		depth_map = self.get_depth_map(img)
		detected_stuff = self.get_object_bounding_boxes(img)
		
		sentence=""
		for i in range(5):
			label=detected_stuff[i][0]
			locations=list(map(int,detected_stuff[i][2])) #convert to int
			locations = [0 if x < 0 else x for x in locations] #replace negative with zeros
			
			cropped_img = depth_map[locations[0]:locations[2],locations[1]:locations[3]]
			#cv2.imshow('dst_rt', cropped_img)
			#cv2.waitKey(3000)
			#cv2.destroyAllWindows()
			mean=cropped_img.flatten().mean()
			#print(mean)
			if (mean>=0 and mean<=85):
				sentence+=f"a {label} is pretty far from you,"
			elif (mean>85 and mean <=170):
				sentence+=f"a {label} is further away,"
			elif (mean>170):
				sentence+=f"a {label} is nearby,"
			else:
				sentence+=f"a {label} has been detected,"
			
		sentence = sentence[:-1]+"."
		return sentence
		print(sentence)
			
		

'''
img = cv2.imread('table.jpg', cv2.IMREAD_UNCHANGED)
obj=SceneDescribe('lite-model_midas_v2_1_small_1_lite_1.tflite','efficientdet_lite0.tflite')
s=time.time()
obj.describe(img)
print(time.time()-s)
'''
