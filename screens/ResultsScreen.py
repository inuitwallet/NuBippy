from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock


class ResultsScreen(Screen):
	"""
		The screen that displays the results to the user
	"""

	def __init__(self, BippyApp, **kwargs):
		super(ResultsScreen, self).__init__(**kwargs)
		self.BippyApp = BippyApp

		self.mainLayout = self.ids.mainLayout.__self__
		self.mainLabel = self.ids.mainLabel.__self__
		self.topLabel = self.ids.topLabel.__self__
		self.topField = self.ids.topField.__self__
		self.middleLabel = self.ids.middleLabel.__self__
		self.middleField = self.ids.middleField.__self__
		self.bottomLabel = self.ids.bottomLabel.__self__
		self.bottomField = self.ids.bottomField.__self__
		return

	def switch_to_results(self, dt):
		"""
			switch to the results screen
		"""
		self.BippyApp.mainScreenManager.transition = SlideTransition(direction='right')
		self.BippyApp.mainScreenManager.current = self.BippyApp.get_string('Results_Screen')
		return

	def display_bip(self, BIP, bAddress, sAddress):
		"""
			Display the BIP encrypted key, the address and the links
		"""
		self.mainLayout.clear_widgets()
		self.mainLayout.add_widget(self.mainLabel)
		self.mainLayout.add_widget(self.topLabel)
		self.mainLayout.add_widget(self.topField)
		self.mainLayout.add_widget(self.middleLabel)
		self.mainLayout.add_widget(self.middleField)
		self.mainLayout.add_widget(self.bottomLabel)
		self.mainLayout.add_widget(self.bottomField)

		Clock.schedule_once(self.switch_to_results, 0.5)

		self.mainLabel.text = self.BippyApp.get_string('Bip_Successful')
		self.topLabel.text = self.BippyApp.get_string('Bip_Key_Label')
		self.topField.text = str(BIP)
		self.middleLabel.text = self.BippyApp.get_string('NuBits_Address_Label')
		self.middleField.text = str(bAddress)
		self.bottomLabel.text = self.BippyApp.get_string('NuShares_Address_Label')
		self.bottomField.text = str(sAddress)
		self.canvas.ask_update()
		return

	def display_wif(self, WIF, bAddress, sAddress):
		"""
			Display the decrypted WIF key, the address and the links
		"""
		self.mainLayout.clear_widgets()
		self.mainLayout.add_widget(self.mainLabel)

		if WIF is False or bAddress is False or sAddress is False:
			self.mainLabel.text = self.BippyApp.get_string('Bip_Decrypt_Unsuccessful')
			return

		self.mainLayout.add_widget(self.topLabel)
		self.mainLayout.add_widget(self.topField)
		self.mainLayout.add_widget(self.middleLabel)
		self.mainLayout.add_widget(self.middleField)
		self.mainLayout.add_widget(self.bottomLabel)
		self.mainLayout.add_widget(self.bottomField)

		Clock.schedule_once(self.switch_to_results, 0.5)

		self.mainLabel.text = self.BippyApp.get_string('Bip_Decrypt_Successful')
		self.topLabel.text = self.BippyApp.get_string('Wif_Key_Label')
		self.topField.text = str(WIF)
		self.middleLabel.text = self.BippyApp.get_string('NuBits_Address_Label')
		self.middleField.text = str(bAddress)
		self.bottomLabel.text = self.BippyApp.get_string('NuShares_Address_Label')
		self.bottomField.text = str(sAddress)
		self.canvas.ask_update()
		return
		
		

