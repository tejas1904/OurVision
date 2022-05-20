import pytessy as pt
from PIL import ImageFilter, Image






if __name__ == "__main__":

	# Create pytessy instance
	ocrReader = pt.PyTessy()

	files = ["cell_pic.jpg"]

	for file in files:
		# Load Image
		img = Image.open(file)

		# Scale up image
		w, h = img.size
		img = img.resize((2 * w, 2 * h))
		# Sharpen image
		img = img.filter(ImageFilter.SHARPEN)
		# Convert to ctypes
		imgBytes = img.tobytes()
		bytesPerPixel = int(len(imgBytes) / (img.width * img.height))
		# Use OCR on Image
		imageStr = ocrReader.read(img.tobytes(), img.width, img.height, bytesPerPixel, raw=True, resolution=600)

		print(file, imageStr)
