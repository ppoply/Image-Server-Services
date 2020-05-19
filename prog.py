
import urllib
import requests
import json
import cv2
import numpy as np


class ImageServer:


	def __init__(self, server_name):
		
		self.server_name = server_name
		self.image_servers = []


	def get_services(self):
		# method for retrieving all Services (including the ones in the folders)
		url = self.server_name + '/rest/services'
		payload = {'f': 'json'}
		json_data = requests.get(url, params = payload).json()		# retrieving json response

		folders = json_data['folders']
		services = json_data['services']

		for folder_name in folders:				# checking for services present in folders
			json_folder_data = requests.get(url+'/' + folder_name, params = payload).json()
			services.extend(json_folder_data['services'])

		return services


	def get_image_servers(self, services):
		# method for finding all items of type ImageServer from the retrieved services
		for server in services:
			#print(server)
			if(server['type'] == 'ImageServer'):
				self.image_servers.append(server['name'])		# if item of type ImageServer then append to image-servers list

		return self.image_servers


	def print_image_servers(self):
		# method for displaying detected ImageServers
		print("List of items of type ImageServer : \n")
		
		for i in self.image_servers:
			print(i)



class ImageService:


	def __init__(self, image_server, image_service):
		
		self.image_server = image_server 	# Object of type ImageServer
		self.image_service = image_service  # User input Image service


	def get_service_information(self):
		# method for retrieving service information
		if(self.image_service not in (self.image_server).image_servers):
			
			print("Image Service not found in the Image Servers list")

		else:

			print("Service found in the Image Servers List")
			url = self.generate_url()
			print('Generated URL for the Image Service : ', url)
			
			payload = {'f': 'json'}
			json_data = requests.get(url, params = payload).json()

			return json_data


	def generate_url(self):
		# method for generating Image service URL
		return (self.image_server).server_name + '/rest/services' + '/' + self.image_service + '/ImageServer'


	def display_service_info(self, json_data):
		# method for displaying Service information (in a pretty way)
		print("\nDisplaying Service Information : ")
		print('\n', json.dumps(json_data, indent = 4))


	def export_image(self, bbox):
		# method for exporting an image
		url = self.generate_url() + '/exportImage'
		payload = {'f': 'json', 'bbox': bbox}
		json_data = requests.get(url, params = payload).json()
		print("Displaying (image) json response : \n", json_data)

		payload = {'f': 'image', 'bbox': bbox}
		img_resp = requests.get(url, params = payload, stream=True).raw		# retrieving image (in raw byte format)
		self.display_image(img_resp)

	
	def display_image(self, resp):
		# method for displaying and writing/saving an image to current directory 
		print("\nDisplaying and writing the exported image.\n")
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)

		cv2.imshow('image', image)
		cv2.imwrite('export_output.png', image)		# writing image as export_output.png in current directory

		cv2.waitKey(0)			# press any key to exit (while image window is selected)
		cv2.destroyAllWindows()


#main
if __name__ == '__main__':

	server = ImageServer('https://sampleserver6.arcgisonline.com/arcgis')		# creating ImageServer instance

	services = server.get_services()		# retrieving services
	image_servers = server.get_image_servers(services)		#	finding all items of type ImageServers

	server.print_image_servers()		# displaying names of all items of type ImageServer

	print("\nno. of Image Servers found : ", len(image_servers), '\n')		# displaying the count of detected ImageServers

	service = ImageService(server, 'ScientificData/SeaTemperature')		# creating ImageService Instance
	service_info = service.get_service_information()		# retrieving ImageService info
	service.display_service_info(service_info)				# displaying ImageService info
	service.export_image('-179.99999999999997,-80.03999717699992,180.0,80.0400028230001')	# exporting image wrt the passed bbox coordinates


