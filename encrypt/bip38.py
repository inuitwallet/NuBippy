import hashlib
import binascii

import encrypt.aes as aes
import encrypt.scrypt as scrypt
import num.enc as enc


def encrypt(privK, Baddress, Saddress, passphrase):
	"""
		BIP0038 private key encryption, Non-EC
	"""
	
	#1. take the first four bytes of SHA256(SHA256(address)) of it. Let's call this "addresshash".
	addresshash = hashlib.sha256(hashlib.sha256(Baddress + Saddress).digest()).digest()[:4]

	#2. Derive a key from the passphrase using scrypt
	#	 a.  Parameters: passphrase is the passphrase itself encoded in UTF-8.
	#		 addresshash came from the earlier step, n=16384, r=8, p=8, length=64
	#		 (n, r, p are provisional and subject to consensus)
	key = scrypt.hash(passphrase, addresshash, 16384, 8, 8)
	
	#Let's split the resulting 64 bytes in half, and call them derivedhalf1 and derivedhalf2.
	derivedhalf1 = key[0:32]
	derivedhalf2 = key[32:64]
	
	#3. Do AES256Encrypt(bitcoinprivkey[0...15] xor derivedhalf1[0...15], derivedhalf2), call the 16-byte result encryptedhalf1
	Aes = aes.Aes(derivedhalf2)
	encryptedhalf1 = Aes.enc(enc.sxor(privK[:16], derivedhalf1[:16]))
	
	#4. Do AES256Encrypt(bitcoinprivkey[16...31] xor derivedhalf1[16...31], derivedhalf2), call the 16-byte result encryptedhalf2
	encryptedhalf2 = Aes.enc(enc.sxor(privK[16:32], derivedhalf1[16:32]))
	
	#5. The encrypted private key is the Base58Check-encoded concatenation of the following, which totals 39 bytes without Base58 checksum:
	#		0x01 0x42 + flagbyte + salt + encryptedhalf1 + encryptedhalf2
	flagbyte = chr(0b11100000)  # 11 no-ec 1 compressed-pub 00 future 0 ec only 00 future
	privkey = ('\x01\x42' + flagbyte + addresshash + encryptedhalf1 + encryptedhalf2)
	check = hashlib.sha256(hashlib.sha256(privkey).digest()).digest()[:4]
	return enc.b58encode(privkey + check)
	
def decrypt(encrypted_privkey, passphrase):
	
	#1. Collect encrypted private key and passphrase from user.
	#	passed as parameters
	data = enc.b58decode(encrypted_privkey)
	flagbyte = data[2:3]
	check = data[-4:]
	if check != hashlib.sha256(hashlib.sha256(data[:-4]).digest()).digest()[:4]:
		return False, 'checksum'

	addresshash = data[3:7]
	encryptedhalf1 = data[7:23]
	encryptedhalf2 = data[23:39]

	#3. Derive decryption key for seedb using scrypt with passpoint, addresshash, and ownersalt
	key = scrypt.hash(passphrase, addresshash, 16384, 8, 8)

	derivedhalf1 = key[0:32]
	derivedhalf2 = key[32:64]

	#4. Decrypt encryptedpart2 using AES256Decrypt to yield the last 8 bytes of seedb and the last 8 bytes of encryptedpart1.
	Aes = aes.Aes(derivedhalf2)
	decryptedhalf2 = Aes.dec(encryptedhalf2)
	
	#5. Decrypt encryptedpart1 to yield the remainder of seedb.
	decryptedhalf1 = Aes.dec(encryptedhalf1)

	priv = decryptedhalf1 + decryptedhalf2
	priv = binascii.unhexlify('%064x' % (long(binascii.hexlify(priv), 16) ^ long(binascii.hexlify(derivedhalf1), 16)))
	return priv, addresshash

