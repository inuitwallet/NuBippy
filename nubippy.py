"""
	bippy.
	Simple tool for enabling BIP 38 encryption of a variety of crypto-currency private keys

	Sponsored by http://woodwallets.io
	Written by the creator of inuit (http://inuit-wallet.co.uk)
"""

from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '400')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation
from kivy.uix.actionbar import ActionBar
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.popup import Popup

from kivy.lang import Builder

import json

import screens.PrivateKeyScreen as PrivateKeyScreen
import screens.ResultsScreen as ResultsScreen


class TopActionBar(ActionBar):
	"""
		The top Action Bar
	"""

	def __init__(self, **kwargs):
		super(TopActionBar, self).__init__(**kwargs)
		#self.infoButton = self.ids.topInfoButton.__self__

	def reset_ui(self):
		"""
			clear all input text from ui
		"""
		BippyApp.mainScreenManager.transition = SlideTransition(direction='left')
		BippyApp.mainScreenManager.current = BippyApp.get_string('Private_Key_Screen')
		BippyApp.reset_ui()
		return


class NubippyApp(App):
	"""
		The application Class for Bippy
	"""

	#Set the language and load the language file
	language = 'english'
	try:
		lang = json.load(open('res/json/languages/' + language + '.json', 'r'))
	except ValueError as e:
		print('')
		print('##################################################################')
		print('')
		print('There was an Error loading the ' + language + ' language file.')
		print('')
		print(str(e))
		print('')
		print('##################################################################')
		raise SystemExit

	def __init__(self, **kwargs):
		super(NubippyApp, self).__init__(**kwargs)
		self.isPopup = False
		self.show_info = False
		return

	def build(self):
		"""
			Build the Main Application Window
		"""
		#Root widget is a Box Layout
		self.root = BoxLayout(orientation='vertical')

		self.infoText = TextInput(readonly=True)
		self.mainScreenManager = ScreenManager(transition=SlideTransition(direction='left'))

		#Add the Action Bar
		self.topActionBar = TopActionBar()
		self.root.add_widget(self.topActionBar)

		#Add the Scroll View For displaying Info
		self.infoScrollView = ScrollView(size_hint_y=None, height=0, border=1)
		self.infoScrollView.add_widget(self.infoText)
		self.root.add_widget(self.infoScrollView)

		#Add the screenManager
		Builder.load_file('screens/PrivateKeyScreen.kv')
		self.privateKeyScreen = PrivateKeyScreen.PrivateKeyScreen(self)
		Builder.load_file('screens/ResultsScreen.kv')
		self.resultsScreen = ResultsScreen.ResultsScreen(self)
		BippyApp.mainScreenManager.add_widget(self.privateKeyScreen)
		BippyApp.mainScreenManager.add_widget(self.resultsScreen)

		self.root.add_widget(BippyApp.mainScreenManager)

		return self.root

	def set_info(self, info):
		"""
			Read the info from the <language>.json file and set it as the info text
		"""
		self.infoText.text = BippyApp.get_string(info)
		return

	def toggle_info(self):
		"""
			This method toggles the visibility of the 'info' space
			It also handles the transition animation of the opening and closing
		"""
		self.show_info = not self.show_info
		if self.show_info:
			height = self.root.height * .3
		else:
			height = 0
		Animation(height=height, d=.3, t='out_quart').start(self.infoScrollView)
		self.topActionBar.infoButton.state = 'normal'

	def reset_ui(self):
		"""
			reset the UI to it's original state
			this is called when the home screen is selected
		"""
		self.privateKeyScreen.reset_ui(None)
		return

	def show_popup(self, title, text):
		"""
			display a modal popup.
			used for error display
		"""
		content = BoxLayout(orientation='vertical')
		content.add_widget(Label(text=text, size_hint=(1,.7)))
		button = Button(text=self.get_string('OK'), size_hint=(1,.3))
		content.add_widget(button)
		self.popup = Popup(title=title, content=content, auto_dismiss=False, size_hint=(None, None), size=(500, 200))
		button.bind(on_press=self.close_popup)
		self.popup.open()
		self.isPopup = True
		return

	def close_popup(self, instance, value=False):
		"""
			Close the warning popup
		"""
		self.popup.dismiss()
		self.isPopup = False
		return

	def get_string(self, text):
		"""
			return the value for the provided string from the language json file
		"""
		try:
			return_string = self.lang[text]
		except (ValueError, KeyError):
			return_string = 'Language Error'
		return return_string

if __name__ == '__main__':
	BippyApp = NubippyApp()
	BippyApp.run()
