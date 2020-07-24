import cv2
import numpy as np
import KNN
import copy
from scipy.stats import mode


def crop_frame(frame, not_needed_below):
	"""
	return frame without non-sky elements
	"""
	return frame[:not_needed_below, :]


def assign_color(name):
	color = None
	if name == 0:
		# for cloud
		color = (255, 0, 0)
	elif name == 1:
		# for sky
		color = (255, 255, 255)
	elif name == 2:
		# for sun
		color = (255, 255, 255)
	return color


def find_clouds(frame, data, image_width=640, image_height=480, step=10):
	"""
	KNN algorithm is used
	"""

	frame = cv2.resize(frame, (image_width, image_height))
	detected = copy.copy(frame)
	sky_array = np.zeros((image_height//step, image_width//step))

	for row in range(0, image_height, step):

		for column in range(0, image_width, step):
			segment = frame[row:row + step, column:column + step]
			histogram = KNN.get_histogram(segment)
			belongs_to = KNN.knn(histogram, data)
			sky_array[row//step, column//step] = belongs_to
			detected[row:row + step, column:column + step] = assign_color(belongs_to)

	return sky_array, detected


def moving_where(source):
	cap = cv2.VideoCapture(source)
	frame_previous = cap.read()[1]
	gray_previous = cv2.cvtColor(frame_previous, cv2.COLOR_BGR2GRAY)
	# set some parameters
	param = {
		'pyr_scale': 0.5,
		'levels': 3,
		'winsize': 15,
		'iterations': 3,
		'poly_n': 5,
		'poly_sigma': 1.1,
		'flags': cv2.OPTFLOW_LK_GET_MIN_EIGENVALS
	}

	while True:
		grabbed, frame = cap.read()
		if not grabbed:
			break

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(gray_previous, gray, None, **param)
		mag, ang = cv2.cartToPolar(flow[:, :, 0], flow[:, :, 1], angleInDegrees=True)

		move_sense = ang[mag > 50.0]
		mode_ang = mode(move_sense)[0]
		print(mode_ang)

	cap.release()
