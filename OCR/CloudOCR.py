import glob
import os
import io
import string
from google.cloud import vision

class CloudOCR:
	
	def __init__(self,api_key_path='/home/pi/Desktop/OurVision/Api_Keys/ourvision-key.json'):
		os.environ['GOOGLE_APPLICATION_CREDENTIALS']=api_key_path
		self.client=vision.ImageAnnotatorClient()
	
	def ocr(self,image_path=None):
		#image_path=os.path.abspath('C:/Users/tejas/OneDrive/Desktop\sales-a5-flyer-with-photo-template_52683-65915.webp')
		with io.open(image_path, 'rb') as image_file:
				content = image_file.read()

		image = vision.Image(content=content)

		response = self.client.text_detection(image=image)
		texts = response.text_annotations

		# final=get_string(texts)
		# print(final)
		#print(texts[0].description)
		return texts[0].description

#redundant function as texts[0] already gives full text
	def get_string(texts):
		final_string=""

		for text in texts:
			if(text.description=='\n'):
				return final_string
			else:
				final_string +=" "+text.description

			return final_string

if __name__ == "__main__":
    obj=CloudOCR()
    s=obj.ocr('/home/pi/Desktop/OurVision/TejasTextDetection/bread.jpeg')
    print(s)




