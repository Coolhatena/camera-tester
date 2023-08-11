import cv2 as cv
import numpy as np

import cameraTesterConfig

# Open the cam (use 0 for the default camera)
cam = cv.VideoCapture(0)

cv.namedWindow('Frame')
cv.namedWindow('Extra frame')

def getPercentage(msk):
	# Count the number of matching pixels
	matching_pixels = cv.countNonZero(msk)

	# Calculate the total number of pixels
	total_pixels = msk.size

	# Calculate the percentage of matching pixels
	percentage_matching = (matching_pixels / total_pixels) * 100

	return percentage_matching


if not cam.isOpened():
	print("Error: Unable to access the cam.")
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
				
				percentage_matching = getPercentage(msk)
				percentage_color = (0, 255, 0) if percentage_matching > 80 else (0, 0, 255)
				filtered = cv.bitwise_and(img_crop, img_crop, mask= msk)

				frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] = filtered
				cv.putText(frame, f'{int(percentage_matching)}%', (int(roi[0]+roi[3]/5), int(roi[1]+roi[2]/1.6)) ,cv.FONT_HERSHEY_SIMPLEX, 0.4, percentage_color, 1)

			cv.imshow('Frame', frame)
			cv.imshow('Extra frame', filtered)

		# Exit the loop when 'q' key is pressed
		if cv.waitKey(1) & 0xFF == ord('b'):
			break
		
	# Release the cam and close the windows
	cam.release()
	cv.destroyAllWindows()
		