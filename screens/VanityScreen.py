from kivy.uix.screenmanager import Screen
import subprocess
import atexit
import os
from kivy.clock import Clock
from platform import system, architecture

import system.gen as gen


class VanityScreen(Screen):
    """
    Display the actions that work with vanity addresses
    """

    def __init__(self, NuBippyApp, **kwargs):
        super(VanityScreen, self).__init__(**kwargs)

        self.NuBippyApp = NuBippyApp
        self.vanity = ''
        self.timer = None
        self.address = ''
        self.privkey = ''
        self.passphrase = ''
        self.command = []

        self.mainLayout = self.ids.mainLayout.__self__
        self.mainLabel = self.ids.mainLabel.__self__
        self.vanityLabel = self.ids.vanityLabel.__self__
        self.vanityInput = self.ids.vanityInput.__self__
        self.submitButton = self.ids.submitButton.__self__

        self.caseLabel = self.ids.caseLabel.__self__
        self.caseCheck = self.ids.caseCheck.__self__
        self.regexLabel = self.ids.regexLabel.__self__
        self.regexCheck = self.ids.regexCheck.__self__
        self.standardLabel = self.ids.standardLabel.__self__
        self.standardCheck = self.ids.standardCheck.__self__

        self.abortButton = self.ids.abortButton.__self__

        self.yesButtonInfo = self.ids.yesButtonInfo.__self__
        self.noButtonInfo = self.ids.noButtonInfo.__self__
        self.yesButtonEncrypt = self.ids.yesButtonEncrypt.__self__
        self.noButtonEncrypt = self.ids.noButtonEncrypt.__self__

        self.passfieldLabel = self.ids.passfieldLabel.__self__
        self.passfield = self.ids.passfield.__self__
        self.feedback = self.ids.feedback.__self__
        self.checkfieldLabel = self.ids.checkfieldLabel.__self__
        self.checkfield = self.ids.checkfield.__self__
        self.actionButton = self.ids.actionButton.__self__

        self.reset_ui(None)
        return

    def reset_ui(self, dt):
        # set up for first use
        self.mainLayout.clear_widgets()
        self.mainLabel.text = self.NuBippyApp.get_string('Vanity_Intro_Text')
        self.mainLayout.add_widget(self.mainLabel)
        self.mainLayout.add_widget(self.vanityLabel)
        self.vanityInput.text = ''
        self.mainLayout.add_widget(self.vanityInput)
        self.mainLayout.add_widget(self.submitButton)
        self.mainLayout.add_widget(self.caseLabel)
        self.caseCheck.active = False
        self.mainLayout.add_widget(self.caseCheck)
        self.mainLayout.add_widget(self.regexLabel)
        self.regexCheck.active = False
        self.mainLayout.add_widget(self.regexCheck)
        self.mainLayout.add_widget(self.standardLabel)
        self.standardCheck.active = True
        self.mainLayout.add_widget(self.standardCheck)

        self.passfield.text = ''
        self.checkfield.text = ''
        self.passphrase = ''

        self.vanity = ''
        self.timer = None
        self.address = ''
        self.privkey = ''
        return

    def toggle_radio(self, button):
        """
            When the text 'Case insenstive' is clicked, this method is fired to toggle the radio button
        """
        if button == 'case':
            self.caseCheck.active = not self.caseCheck.active
            self.regexCheck.active = not self.caseCheck.active
            self.standardCheck.active = not self.caseCheck.active
        if button == 'regex':
            self.regexCheck.active = not self.regexCheck.active
            self.caseCheck.active = not self.regexCheck.active
            self.standardCheck.active = not self.regexCheck.active
        if button == 'standard':
            self.standardCheck.active = not self.standardCheck.active
            self.caseCheck.active = not self.standardCheck.active
            self.regexCheck.active = not self.standardCheck.active
        return

    def submit_vanity(self, vanity, command=''):
        """
        submit the vanity text and pass it to vanitygen for a test run

        we simulate a full run. This will give us the difficulty and the first three system info outputs
        if the vanity is very easy we may get the address and private key in the output of the simulation
        otherwise we can show an estimation of how long generation will take to the user
        """
        # store the vanity text for later use
        self.vanity = vanity
        startupinfo = None
        # build the command
        if command == '':
            #vanitygen linux
            if system() == 'Linux':
                if architecture()[0] == '64bit':
                    self.command = ['./res/vanitygen/vanitygen_linux_64']
                else:
                    self.command = ['./res/vanitygen/vanitygen_linux']
            #Windows
            if system() == 'Windows':
                startupinfo = subprocess.STARTUPINFO()
                subprocess.STARTF_USESHOWWINDOW = 1
                self.command = ['./res/vanitygen/vanitygen.exe']

            #Mac
            if system() == 'Darwin':
                if architecture()[0] == '64bit':
                    self.command = ['./res/vanitygen/vanitygen_mac_64']
                else:
                    self.command = ['./res/vanitygen/vanitygen_mac']

            if self.caseCheck.active is True:
                self.command.append('-i')

            if self.regexCheck.active is True:
                self.command.append('-r')

            if self.NuBippyApp.chosenCurrency == 'NuBits':
                self.command.append('-X 25#191')
                self.command.append('-n')
                self.command.append('B' + self.vanity)

            if self.NuBippyApp.chosenCurrency == 'NuShares':
                self.command.append('-X 63')
                self.command.append('-n')
                self.command.append('S' + self.vanity)

        try:
            if system() == 'Windows':
                output = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          universal_newlines=True, startupinfo=startupinfo, creationflags=0x8000000)
            else:
                output = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          universal_newlines=True, startupinfo=startupinfo)
        except OSError:
            self.BippyApp.show_popup(self.BippyApp.get_string('Popup_Error'),
                                     self.BippyApp.get_string('Vanity_Run_Error'))
            return

        # first check for errors
        error = output.stderr.read()
        if error != '':
            # there's a few things to try, we can turn on case insensitivity (-i) and try the match as a regex too (-r).
            # try each in turn
            if '-i' not in self.command:
                self.command.append('-i')
                self.submit_vanity(self.vanity, self.command)
                self.NuBippyApp.show_popup(self.NuBippyApp.get_string('Warning'),
                                           self.NuBippyApp.get_string('Case_Sensitivity_Warning'))
                return
            # if we get here, none of the above worked so show the error
            self.NuBippyApp.show_popup(self.NuBippyApp.get_string('Popup_Error'), error)
            return
        # now see if an easy vanity pattern was found during the simulation
        values = output.stdout.read()
        if 'Pattern:' in values:
            self.display_vanity(values)
        else:
            # we have a stdout file object that contains difficulty and three rows of system info.
            # we display that to the user to allow them to decide if they want to undertake the generation
            self.display_system_info(values)
        return

    def get_system_info(self, data1, data2):
        """
        calculate the system information and estimated time to address based on the two lines of good data
        we can return rate, a time estimate with percentage change attached
        units:
            rate -> keys/second
            time -> seconds
            percentage -> percent
        """
        rate = int((int(data1.split('|')[0]) + int(data2.split('|')[0])) / 2)
        percentage = int((int(data1.split('|')[1]) + int(data2.split('|')[1])) / 2)
        time = int((int(data1.split('|')[2]) + int(data2.split('|')[2])) / 2)
        return rate, time, percentage

    def display_system_info(self, values):
        """
        show the system information from the vanitygen simulation process to the user
        """
        # if regex search, we don't have info like this
        if '-r' in self.command:
            output = self.NuBippyApp.get_string('Regex_Search_Info')
        else:
            val = values.split('\n')
            # first row is difficulty
            difficulty = val[0].split(':')[1].strip()
            #next three lines are system info
            #we are only really interested in the last two though as the first never seems to give the correct estimates
            #send that necessary data to the function for parsing
            rate, time, percentage = self.get_system_info(val[2], val[3])

            #unit conversion of rate and time
            rate_unit = 'keys/sec'
            if rate > 1000:
                rate = (rate / 1000)
                rate_unit = 'Kkeys/sec'
            if rate > 1000:
                rate = (rate / 1000)
                rate_unit = 'Mkeys/sec'

            time_unit = 'seconds'
            if time > 60:
                time = (time / 60)
                time_unit = 'minutes'
            if time > 60:
                time = (time / 60)
                time_unit = 'hours'
            if time > 24:
                time = (time / 24)
                time_unit = 'days'
            if time > 365:
                time = (time / 365)
                time_unit = 'years'

            output = self.NuBippyApp.get_string(
                'System_Info_1') + self.NuBippyApp.chosenCurrency + self.NuBippyApp.get_string(
                'System_Info_2') + self.vanity \
                     + self.NuBippyApp.get_string('System_Info_3') + difficulty + self.NuBippyApp.get_string(
                'System_Info_4') \
                     + self.NuBippyApp.get_string('System_Info_5') + str(rate) + ' ' + rate_unit + '.' \
                     + self.NuBippyApp.get_string('System_Info_6') + str(percentage) + self.NuBippyApp.get_string(
                'System_Info_7') \
                     + str(time) + ' ' + time_unit + self.NuBippyApp.get_string('System_Info_8')

        self.mainLayout.clear_widgets()
        self.mainLayout.add_widget(self.mainLabel)
        self.mainLabel.text = output
        self.mainLayout.add_widget(self.yesButtonInfo)
        self.mainLayout.add_widget(self.noButtonInfo)
        return

    def show_password(self):
        """
        set up the ui ready for password entry
        """
        self.mainLayout.clear_widgets()
        self.mainLabel.text = self.NuBippyApp.get_string('Vanity_Passphrase')
        self.mainLayout.add_widget(self.mainLabel)
        self.mainLayout.add_widget(self.passfieldLabel)
        self.mainLayout.add_widget(self.passfield)
        self.mainLayout.add_widget(self.feedback)
        self.mainLayout.add_widget(self.checkfieldLabel)
        self.mainLayout.add_widget(self.checkfield)
        self.passfield.focus = True
        return

    def check_passphrase(self, passfield, checkfield, feedback, layout, button):
        """
        Check that the entered passphrase confirms to the basic rules
        ialso check that the confirmation matches the original
        """

        layout.remove_widget(button)

        # get the text we need to compare
        passphrase = passfield.text
        checktext = checkfield.text

        # check for tabs in the passphrase or check string.
        #tabs don't do anything as standard so we check for them and move the focus accordingly
        if '\t' in passphrase:
            passfield.text = passphrase.replace('\t', '')
            checkfield.focus = True
            return
        if '\t' in checktext:
            checkfield.text = checktext.replace('\t', '')
            passfield.focus = True
            return

        #check the passphrase against the rules
        if len(passphrase) < 1:
            feedback.text = ''
            return
        if 7 > len(passphrase) > 0:
            feedback.color = (0.93725, 0.21176, 0.07843, 1)
            feedback.text = self.NuBippyApp.get_string('Passphrase_Too_Short')
            return
        elif passphrase != checktext:
            feedback.color = (1, 0.72157, 0, 1)
            feedback.text = self.NuBippyApp.get_string('Passphrases_Dont_Match')
            return
        else:
            feedback.text = ''
            button.text = self.NuBippyApp.get_string('Encrypt')
            layout.add_widget(button)
            self.passphrase = passphrase
            return

    def update_counter(self, dt):
        """
        Update the timer on the mainLabel
        """
        self.timer = 1 if self.timer is None else (self.timer + 1)
        minutes = (self.timer / 60)
        hours = (minutes / 60)
        days = (hours / 24)
        years = (days / 365)
        seconds = self.timer % 60
        counter = (str(years).zfill(2) + ' years ') \
                  + (str(days).zfill(2) + ' days ') \
                  + (str(hours).zfill(2) + ' hours ') \
                  + (str(minutes).zfill(2) + ' minutes ') \
                  + str(seconds).zfill(2) + ' seconds'
        self.mainLayout.clear_widgets()
        self.mainLabel.text = self.NuBippyApp.get_string('Starting_Search') + '\n\n\n' \
                              + self.NuBippyApp.get_string('Approximate_Time') + '\n' + counter
        self.mainLayout.add_widget(self.mainLabel)
        self.mainLayout.add_widget(self.abortButton)
        return

    def read_output(self, dt):
        """
            read the output of the vanitygen program and see if an address has been found
        """
        line = self.output.stdout.readline()
        if 'Address:' in line:
            Clock.unschedule(self.update_counter)
            Clock.unschedule(self.read_output)
            line += self.output.stdout.readline()
            self.display_vanity(line)
        return

    def abort_vanitygen(self):
        """
            kill the vanitygen search and reset the ui
        """
        Clock.unschedule(self.update_counter)
        Clock.unschedule(self.read_output)
        os.kill(self.output.pid, 2)
        self.reset_ui(None)
        return

    def run_vanitygen(self):
        """
            run the vanitygen executable without the 'simulate' flag
        """
        self.counter = Clock.schedule_interval(self.update_counter, 1)
        self.reader = Clock.schedule_interval(self.read_output, 0.1)
        # self.command contains the full command we tested with so should work first time
        self.command.remove('-n')
        startupinfo = None
        if system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.output = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True, startupinfo=startupinfo)

        def kill_vanitygen():
            """
            kill the vanitygen process.
            designed to be called atexit to cancel any unwanted long-running process
            """
            self.abort_vanitygen()
            return

        atexit.register(kill_vanitygen)
        return

    def display_vanity(self, values):
        """
        show the results of the vanitygen process to the user
        """
        lines = values.split('\n')
        for line in lines:
            if 'Address:' in line:
                self.address = line.split(':')[1].strip()
            if 'Privkey:' in line:
                self.privkey = line.split(':')[1].strip()
        self.mainLayout.clear_widgets()
        self.mainLayout.add_widget(self.mainLabel)
        self.mainLayout.add_widget(self.yesButtonEncrypt)
        self.mainLayout.add_widget(self.noButtonEncrypt)
        self.mainLabel.text = self.NuBippyApp.get_string('Display_Vanity_1') + self.address \
                              + self.NuBippyApp.get_string('Display_Vanity_2')
        return

    def display_result(self):
        """
        set up the results page and pass the variables to them
        """
        resultsScreen = self.NuBippyApp.mainScreenManager.get_screen('Results')
        resultsScreen.display_wif_vanity(self.privkey, self.address)

    def encrypt_privkey(self):
        """
        BIP0038 encrypt the generated private key
        """
        self.mainLayout.clear_widgets()
        self.mainLabel.text = self.NuBippyApp.get_string('Starting_Bip')
        self.mainLayout.add_widget(self.mainLabel)
        Clock.schedule_once(self.encrypt, 0.5)

    def encrypt(self, dt):
        """
        Perform the actual encryption
        """
        BIP, bAddress, sAddress = gen.encBIPKey(self.privkey, self.passphrase)
        resultsScreen = self.NuBippyApp.mainScreenManager.get_screen('Results')
        resultsScreen.display_bip(BIP, bAddress, sAddress)

        # clear the UI
        Clock.schedule_once(self.reset_ui, 5)
