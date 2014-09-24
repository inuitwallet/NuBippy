import re
import json
import hashlib
import num.enc as enc

def isWif(key):
	if re.search("^[a-km-zA-HJ-NP-Z0-9]{52}", key):
		if checkChecksum(key):
			return True, 'compressed'
		else:
			return True, 'badchecksum'
	if re.search("^[a-km-zA-HJ-NP-Z0-9]{51}", key):
		if checkChecksum(key):
			return True, 'uncompressed'
		else:
			return True, 'badchecksum'
	else:
		return False, 'notwif'

def isBip(key):
	if re.search('^6P[a-km-zA-HJ-NP-Z0-9]{56}$', key):
		if checkChecksum(key):
			return True, 'good'
		else:
			return True, 'badchecksum'
	else:
		return False, 'bad'
		
def isHex(key):
	if re.search('[0-9A-F]{64}$', key):
		return True
	else:
		return False
		
def isBase64(key):
	if re.search('^[A-Za-z0-9=+\/]{44}$', key):
		return True
	else:
		return False
		
def isBase6(key):
	if re.search('^[1-6]{99}$', key):
		return True
	else:
		return False

def privKeyVersion(privK):
	"""
		determine what sort of private key we have
		convert it to raw (base 10) and return

		No need to alert to a bad checksum as this should have already been checked in the input check
	"""
	isWIF, comment = isWif(privK)
	if isWIF is True:
		privK = enc.decode(enc.encode(enc.decode(privK, 58), 256)[1:-5], 256)
	elif isHex(privK):
		privK = enc.decode(privK, 16)
	elif isBase64(privK):
		privK = privK.decode('base64', 'strict')
	elif isBase6(privK):
		privK = privK.decode('base6', 'strict')
	return privK

def checkChecksum(key):
	"""
		requires a base58_Check encoded string.
		calculates the hash of the key and compare to the checksum
	"""
	#decode to base256
	checkKey = enc.b58decode(key)
	checksum = checkKey[-4:]
	hash = hashlib.sha256(hashlib.sha256(checkKey[:-4]).digest()).digest()[:4]
	if hash == checksum:
		return True
	else:
		return False
