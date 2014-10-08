#NuBippy 
###fast and easy BIP0038 encryption and vanity addresses for NuBits and NuShares

NuBippy is a port of Bippy [https://github.com/inuitwallet/bippy] specifically for NuBits and NuShares [https://nubits.com/]

NuBippy is able to generate valid NuBit and NuShare private keys and addresses. It uses a customised BIP0038 encryption method [https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki] to add passphrase protected encryption to the private keys. Using a customised version of vanitygen [https://github.com/inuitwallet/vanitygen], Nubippy is able to generate vanity addresses for NuBits or NuShares and offer optional BIP0038 style encryption on those private keys too.

###Installing NuBippy

Nubippy is built using Python 2.7 [https://www.python.org/downloads/] and Kivy [http://kivy.org/#download]. 
Both will need to be installed on your computer before Nubippy will run. There are good instructions for installing both Python and Kivy on their respective websites. 

On Windows Kivy comes as a portable application. It can be a bit of a faff to get it working first time but the instructions on the Kivy site are clearer than I can manage here.
I intend to build some binary versions of NuBippy in the near future which should make this step unneccessary. I will update this README when that happens.

###Runing NuBippy

Once you have Python and Kivy installed simply clone this repository and run the NuBippy.py file
The command used differs on different OSes. On Linux you use 'python NuBippy.py'. On Mac you use 'kivy NuBippy.py'. On windows you have to go through the procedure laid out on the Kivy website. 
Again, once I have compiled some executable versions, this will be unneccessary.

###Using NuBippy






