import requests
import cv2

class Utils:
	
	def __init__(self):
		self.BASE_URL = "http://54.157.12.31:5000/image/upload/"
		self.BASE_DIR = "../images/cap_{num}.jpg"
		self.num = 0

	def post(self, img_num):
		image = open(self.BASE_DIR.format(num=img_num), 'rb')
		upload = {'file': image}
		r = requests.post(self.BASE_URL, files=upload)
		if r is None:
			return False
		return self.BASE_URL

	def capture(self, camera):
		ret, img = camera.read()
		if ret:
			self.num += 1
			cv2.imwrite('../images/cap_{num}.jpg'.format(num=self.num), img)
			return self.num
		return -1

	def close(self, camera):
		if camera:
			camera.release()
			return True
		return False
