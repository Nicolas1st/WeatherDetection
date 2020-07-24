import cv2
import ephem


class Camera:

	cameras_overall = 0

	def __init__(self, latitude, longitude, direction):

		self.number_in_system = Camera.cameras_overall

		try:
			self.video_stream = cv2.VideoCapture(self.number_in_system)
			self.video_stream.release()
			Camera.cameras_overall += 1
		except:
			print("""The camera is not not found.
			It can be so for two reasons:
			1) The other instance is using the camera,
			try to remove the one that is not needed.
			2) There is no camera in the system.
			""")

		self.location = ephem.Observer()
		self.location.lat = str(latitude)
		self.location.long = str(longitude)
		self.direction = direction
		self.working = False

	def get_working_hours(self):
		"""
		return tuple with two time boundaries
		"""
		o = ephem.Observer()
		o.lat = self.latitude
		o.long = self.longitude
		s = ephem.Sun()
		s.compute()
		ephem.localtime(o.next_rising(s))
		rising_at = ephem.localtime(o.next_rising(s))
		setting_at = ephem.localtime(o.next_setting(s))
		return rising_at, setting_at

	def is_working_hours(self):
		sun = ephem.Sun(self.location)
		sun_is_up = self.location.previous_rising(sun) > self.location.previous_setting(sun)
		return sun_is_up

	# complete it
	def set_direction(self, direction):
		"""
		direction is set in degrees

			  N			N = 0 degrees
			  |			
			  |		E = 90 degrees
			  |			
		W-----------E	S = 180 degrees
			  |			
			  |			W = 270 degrees
			  |			
			  S
		"""
		self.direction = direction % 360

	# complete it
	def set_coordinates(self, latitude, longitude):
		"""
		Used in case the camera is relocated.
		Coordinates are set in degrees.
		"""
		self.latitude = latitude
		self.longitude = longitude
		self.location.lat = latitude
		self.location.long = longitude

	def get_frame(self):
		ret, frame = self.video_stream.read()
		return frame

	def start(self):
		if not self.working and self.is_working_hours():
			self.video_stream = cv2.VideoCapture(self.number_in_system)

	def stop(self):
		if self.working:
			self.video_stream.release()

	def __del__(self):
		Camera.cameras_overall -= 1
		print('The instance of the Camera class has been deleted')
