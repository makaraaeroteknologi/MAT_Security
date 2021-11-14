import cv2
import os
import argparse
from network_model import model
from aux_functions import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout	import BoxLayout
from kivy.uix.textinput	import TextInput
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


frame_num = 0
DNN = model()
Window.size = (1280, 720)


# Load apps design
Builder.load_file('mainwindow.kv')


class MainWindow(Widget):
	def playbutton_press(self):
		#opencv2 stuffs
		if self.ids.pause_button.state == 'normal':
			self.ids.play_button.state = 'down'
			self.ids.pause_button.state = 'down'
			if self.ids.connect_button.state== 'normal':
				self.capture = cv2.VideoCapture(0)
				self.video_display = Clock.schedule_interval(self.update, 1.0/30)	
			elif self.ids.connect_button.state == 'down':
				self.capture = cv2.VideoCapture(self.ids.url_input.text + "/screen_stream.mjpeg")
				self.video_display =Clock.schedule_interval(self.update, 1.0/30)

		elif self.ids.pause_button.state == 'down':
			self.ids.play_button.state = 'down'
			self.video_display.cancel()
			self.ids.video_player.source = 'resources/SS_videoimg.png'

	def pausebutton_press(self):
		if self.ids.play_button.state == 'down':	
			self.ids.play_button.state = 'normal'
			self.ids.pause_button.state = 'normal'
			self.video_display.cancel()
			self.capture = 0
			self.ids.video_player.source: 'resources/SS_videoimg.png'
			

		elif self.ids.play_button.state == 'normal':
			self.ids.pause_button.state = 'normal'
			
		
	def update(self,dt):
		# display image from cam in opencv window
		height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
		width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
		fps = int(self.capture.get(cv2.CAP_PROP_FPS))
		global frame_num
		frame_num += 1
		ret, frame = self.capture.read()
		frame = cv2.resize(frame,(892,595),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
		
		pedestrian_boxes, num_pedestrians = DNN.detect_pedestrians(frame)
        
		if len(pedestrian_boxes) > 0:
			pedestrian_detect = plot_pedestrian_boxes_on_image(frame, pedestrian_boxes)
			self.ids.notif_img.source = 'resources/alert.png'
			self.ids.notif_string.text =f'Ada {num_pedestrians} penyusup \nterdeteksi'
		else: 
			self.ids.notif_img.source = 'resources/SS_checkshield.png'
			self.ids.notif_string.text = "Tidak ada penyusup \nterdeteksi"
          
		total = str(num_pedestrians)

		# convert it to texture
		buf1 = cv2.flip(frame, 0)
		buf = buf1.tostring()
		texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

		texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		# display image from the texture
		self.ids.video_player.texture = texture1
		

class MATApp(App):
	def build(self):
		return MainWindow()


if __name__ == '__main__':
	MATApp().run()
	cv2.destroyAllWindows()
