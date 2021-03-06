#NuBippy 
###fast and easy BIP0038 encryption and vanity addresses for NuBits and NuShares

(donations [NBT] : BMJ2PJ1TNMwnTYUopQVxBrAPmmJjJjhd96)

NuBippy is a port of Bippy [https://github.com/inuitwallet/bippy] specifically for NuBits and NuShares [https://nubits.com/]

NuBippy is able to generate valid NuBit and NuShare private keys and addresses. It uses a customised BIP0038 encryption method [https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki] to add passphrase protected encryption to the private keys. Using a customised version of vanitygen [https://github.com/inuitwallet/vanitygen], NuBippy is able to generate vanity addresses for NuBits or NuShares and offer optional BIP0038 style encryption on those private keys too.

###Windows installer

NuBippy has been packaged into an installable file. The download will conatain the installer exe file, the source doe and a README file. It is available here:

http://bippy.org/nubippy


###Installing NuBippy from source

NuBippy is built using Python 2.7 [https://www.python.org/downloads/] and Kivy [http://kivy.org/#download]. 
Both will need to be installed on your computer before NuBippy will run. There are good instructions for installing both Python and Kivy on their respective websites. 


###Running NuBippy

If you used the Windows installer, simply click the link on the desktop or in the start Menu

Otherwise, once you have Python and Kivy installed, clone this repository and run the NuBippy.py file
The command used differs on different OSes. On Linux you use 'python NuBippy.py'. On Mac you use 'kivy NuBippy.py'.

NuBippy can be used totally offline. It also has no cache (unlike a web browser) so the keys it generates can be considered 'cold'.

###Using NuBippy

NuBippy is intended to be simple and to have an obvious workflow. There are instructions given on every action so it should be fairly self explanitory. 
You can choose what action you want to undertake byt selecting from the 'Action' drop down menu on the top bar.
When generating a vanity address, you need to choose either NuBits or NuShares as your currency (default is NuBits). this is done from the second dropdown on the top bar which is only active on the Vanity Address screen. 
To generate a vanity address, just enter the text you want to search for. Don't enter the standard prefix for Nubits ('B') or NuShares ('S') as NuBippy adds these automatically.

If at any point you want to stop the Action and return to the home screen, press the main NuBippy logo on the far left of the top bar. This will reset all the screens and remove any data that has been entered or generated

###The science bit

####BIP0038

The BIP0038 encryption method had to be modified slightly to work with NuBits and NuShares. Each valid private key can be used to hash an address for both NuBits and NuShares. The first step of the BIP0038 method is to generate an 'addresshash' which is added to the encrypted private key output. This is used to verify that the correct private key has been obtained when decryption happens. 
To avoid confusion as to which address to use I decided to concatenate both possible addresses together:

addresshash = sha256(sha256(NuBits_address + Nushares_Address))[:4]

Aside from that change, the BIP0038 method remians the same.

####Vanitygen

The vanitygen binary used by NuBippy has been modified to always generate compressed private and public keys. this keeps it inline with the rest of the private nad public keys NuBippy is able to create.
It has also been modified to accept two version numbers when a different version is specified. This allows for Nubit addresses to be generated which have a different version number to their corresponding private key.

####Entropy

When generating private keys internally, NuBippy uses three different sources of Entropy. The most obvious is the user entered entropy which is collected when you draw dots over NuBippy with your mouse. This is combined with clock based and urandom based entropy to generate random private keys for better security.


###Known Issues

The issues at the moment are to do with the compiling of the binaries that NuBippy needs to run. The two it uses are scrypt (for BIP0038 encryption) and vanitygen (for vanity address generation).
Nubippy currently has scrypt binaries for:
Linux (64 bit)
Linux (32 bit)
OSX (64 bit)
Windows (32 bit)

and vanitygen binaries for:
Linux (64 bit)
Windows (32 bit)

(Windows will only use the 32 bit version of these binaries so only Mac versions are missing)

If you are able to compile vanitygen or scrypt for platforms not mentioned, please do so and share the binary with me. Thanks :)







