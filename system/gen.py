import hashlib

import encrypt.bip38 as bip38
import num.enc as enc
import system.key as key
import num.rand as rand
import system.address as address

def genBIPKey(passphrase, entropy='', privateKey=''):
	"""
		Generate a BIP38 private key + public addresses
	"""
	#generate the private and public keys
	if privateKey == '':
		privateKey = int(rand.randomKey(rand.entropy(entropy)))
	privK256 = enc.encode(privateKey, 256, 32)
	bPublicAddress, sPublicAddress = address.publicKey2Address(address.privateKey2PublicKey(privateKey))
	#BIP38 encryption
	BIP = bip38.encrypt(privK256, bPublicAddress, sPublicAddress, str(passphrase))
	print(decBIPKey(BIP, str(passphrase)))
	return BIP, bPublicAddress, sPublicAddress
	
def encBIPKey(privK, passphrase):
	"""
		Encrypt an existing private key with BIP38
	"""
	#we need to check what type of private key we are working with and change it to raw (base10)
	privK = key.privKeyVersion(privK)
	#once we have this we can use the function above to generate the BIP keys
	BIP, bPublicAddress, sPublicAddress = genBIPKey(passphrase, '', privK)
	return BIP, bPublicAddress, sPublicAddress

def decBIPKey(encrypted_privK, passphrase):
	"""
		Decrypt an encrypted Private key
		Show the corresponding public address
	"""
	privK, addresshash = bip38.decrypt(str(encrypted_privK), str(passphrase))
	privK = enc.decode(privK, 256)
	#calculate the addresses from the key
	bPublicAddress, sPublicAddress = address.publicKey2Address(address.privateKey2PublicKey(privK))
	#check our generated address against the address hash from BIP
	if hashlib.sha256(hashlib.sha256(bPublicAddress + sPublicAddress).digest()).digest()[0:4] != addresshash:
		return False, False, False
	else:
		return address.privateKey2Wif(privK), bPublicAddress, sPublicAddress

def verifyPassword(password):
	"""
		Check the length and complexity of the password
		return true if a pass, false otherwise
	"""
	if len(password) < 7:
		return False
	return True
