from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock


class ResultsScreen(Screen):
    """
        The screen that displays the results to the user
    """

    def __init__(self, NuBippyApp, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.NuBippyApp = NuBippyApp

        self.mainLayout = self.ids.mainLayout.__self__
        self.mainLabel = self.ids.mainLabel.__self__
        self.topLabel = self.ids.topLabel.__self__
        self.topField = self.ids.topField.__self__
        self.middleLabel = self.ids.middleLabel.__self__
        self.middleField = self.ids.middleField.__self__
        self.bottomLabel = self.ids.bottomLabel.__self__
        self.bottomField = self.ids.bottomField.__self__

        self.addressLabel = self.ids.addressLabel.__self__
        self.addressField = self.ids.addressField.__self__
        return

    def switch_to_results(self, dt):
        """
        switch to the results screen
        """
        self.NuBippyApp.mainScreenManager.transition = SlideTransition(direction='right')
        self.NuBippyApp.mainScreenManager.current = self.NuBippyApp.get_string('Results_Screen')
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

        self.mainLabel.text = self.NuBippyApp.get_string('Bip_Successful')
        self.topLabel.text = self.NuBippyApp.get_string('Bip_Key_Label')
        self.topField.text = str(BIP)
        self.middleLabel.text = self.NuBippyApp.get_string('NuBits_Address_Label')
        self.middleField.text = str(bAddress)
        self.bottomLabel.text = self.NuBippyApp.get_string('NuShares_Address_Label')
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
            self.mainLabel.text = self.NuBippyApp.get_string('Bip_Decrypt_Unsuccessful')
            return

        self.mainLayout.add_widget(self.topLabel)
        self.mainLayout.add_widget(self.topField)
        self.mainLayout.add_widget(self.middleLabel)
        self.mainLayout.add_widget(self.middleField)
        self.mainLayout.add_widget(self.bottomLabel)
        self.mainLayout.add_widget(self.bottomField)

        Clock.schedule_once(self.switch_to_results, 0.5)

        self.mainLabel.text = self.NuBippyApp.get_string('Bip_Decrypt_Successful')
        self.topLabel.text = self.NuBippyApp.get_string('Wif_Key_Label')
        self.topField.text = str(WIF)
        self.middleLabel.text = self.NuBippyApp.get_string('NuBits_Address_Label')
        self.middleField.text = str(bAddress)
        self.bottomLabel.text = self.NuBippyApp.get_string('NuShares_Address_Label')
        self.bottomField.text = str(sAddress)
        self.canvas.ask_update()
        return

    def display_wif_vanity(self, WIF, address):
        """
        display the Wif and address from a vanity generation
        """
        self.mainLayout.clear_widgets()
        self.mainLayout.add_widget(self.mainLabel)

        self.mainLayout.add_widget(self.topLabel)
        self.mainLayout.add_widget(self.topField)
        self.mainLayout.add_widget(self.addressLabel)
        self.mainLayout.add_widget(self.addressField)

        Clock.schedule_once(self.switch_to_results, 0.5)

        self.mainLabel.text = self.NuBippyApp.get_string('Vanity_Wif_Text')
        self.topLabel.text = self.NuBippyApp.get_string('Wif_Key_Label')
        self.topField.text = str(WIF)
        if self.NuBippyApp.chosenCurrency == 'NuBits':
            self.addressLabel.text = self.NuBippyApp.get_string('NuBits_Address_Label')
            self.addressLabel.color = (1, 0.72157, 0, 1)
        else:
            self.addressLabel.text = self.NuBippyApp.get_string('NuShares_Address_Label')
            self.addressLabel.color = (0.93725, 0.21176, 0.07843, 1)
        self.addressField.text = str(address)
        self.canvas.ask_update()
        return


