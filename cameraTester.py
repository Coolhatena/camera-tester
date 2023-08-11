import cv2 as cv
import numpy as np

import cameraTesterConfig

# Open the cam (use 0 for the default camera)
cam = cv.VideoCapture(0)

cv.namedWindow('Frame')
cv.namedWindow('Extra frame')

print(cameraTesterConfig.roiColorFilters)

if not cam.isOpened():
	print("Error: Unable to access the webcam.")
else:
	while True:
		# Capture frame-by-frame from the cam
		ret, frame = cam.read()

		roi_color_filters = cameraTesterConfig.roiColorFilters

		if ret:
			for color_data in roi_color_filters: 
				roi = color_data[2]
				img_crop = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
				hsv = cv.cvtColor(img_crop, cv.COLOR_BGR2HSV)
				msk = cv.inRange(hsv, np.array(color_data[0]), np.array(color_data[1]))
				filtered = cv.bitwise_and(img_crop, img_crop, mask= msk)

				frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] = filtered

			cv.imshow('Frame', frame)
			cv.imshow('Extra frame', filtered)

		# Exit the loop when 'q' key is pressed
		if cv.waitKey(1) & 0xFF == ord('b'):
			break
		
	# Release the cam and close the windows
	cam.release()
	cv.destroyAllWindows()
		