import random
import num.rand as rand
import system.address as address
import encrypt.public_address as pub_address
import system.key as key


#build the entropy
entropy = []
entropy.append((int(random.getrandbits(52)), int(random.getrandbits(52))))

privateKey = int(rand.randomKey(rand.entropy(entropy)))
publicAddress = address.publicKey2Address(address.privateKey2PublicKey(privateKey, True), 0, '1', 32)
print(publicAddress)
eAdd = pub_address.encrypt(publicAddress, 's4mm0th')
print(eAdd)
isValid, comment = key.isEncAddress(eAdd)
print(str(isValid) + ' => ' + comment)

newAdd, comment = pub_address.decrypt(eAdd, 's4mm0th')

print(str(newAdd) + ' => ' + comment)
