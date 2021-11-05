import sys
import time

import cv2
from pykinect_azure.k4abt._k4abtTypes import K4ABT_JOINT_NAMES

sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(module_k4abt_path="/usr/lib/libk4abt.so", track_body=True)

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	# Start body tracker
	bodyTracker = pykinect.start_body_tracker()

	cv2.namedWindow('Depth image with skeleton',cv2.WINDOW_NORMAL)
	while True:

		# Get capture
		capture = device.update()

		# Get body tracker frame
		body_frame = bodyTracker.update()  # LOOK HERE

		# Get the color depth image from the capture
		ret, depth_color_image = capture.get_colored_depth_image()

		# Get the colored body segmentation
		ret, body_image_color = body_frame.get_segmentation_image()

		if not ret:
			continue

		# Combine both images
		combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)

		# Draw the skeletons
		combined_image = body_frame.draw_bodies(combined_image) # LOOK HERE

		# Overlay body segmentation on depth image
		cv2.imshow('Depth image with skeleton',combined_image)

		print(body_frame.get_num_bodies())
		#print(body_frame.get_segmentation_image())

		if body_frame.get_num_bodies()==3:
			print(body_frame.handle())

		# raised hand around -700~-1100 units


		#doesntwork print(body_frame.get_body_skeleton(0))
		print("Right Hand X:", body_frame.get_body_skeleton().joints[15].position.xyz.x)
		#print("Right Hand Y:", body_frame.get_body_skeleton().joints[15].position.xyz.y)
		time.sleep(0.2)
		# print("Y:", body_frame.get_body_skeleton().joints[15].position.xyz.y)
		#print("Z:", body_frame.get_body_skeleton().joints[15].position.xyz.z)

		# print("Right Hand")
		# if body_frame.get_body_skeleton().joints[15].position.xyz.y < -580:
		# 	print("High")
		#
		# if body_frame.get_body_skeleton().joints[15].position.xyz.y > 250:
		# 	print("Low")
		#
		# if body_frame.get_body_skeleton().joints[15].position.xyz.x < -300:
		# 	print("Right")
		#
		# if body_frame.get_body_skeleton().joints[15].position.xyz.x > 300:
		# 	print("Left")
		#
		# print("Left Hand")
		# if body_frame.get_body_skeleton().joints[8].position.xyz.y < -580:
		# 	print("High")
		#
		# if body_frame.get_body_skeleton().joints[8].position.xyz.y > 250:
		# 	print("Low")
		#
		# if body_frame.get_body_skeleton().joints[8].position.xyz.x < -300:
		# 	print("Right")
		#
		# if body_frame.get_body_skeleton().joints[8].position.xyz.x > 300:
		# 	print("Left")

		# Press q key to stop
		if cv2.waitKey(1) == ord('q'):
			break