import hashlib

import num.elip as elip
import num.enc as enc


def privateKey2Wif(privateKey, compressed=True):
    """
        Return private key in compressed WIF format
    """
    return base58Encode(enc.encode(privateKey, 256, 32) + '\x01', 191, 'B')


def privateKey2PublicKey(priv, compressed=True):
    """
        integer 256 bit ECC private key to hexstring compressed public key
    """
    pub = elip.base10_multiply(elip.G, priv)
    return '0' + str(2 + (pub[1] % 2)) + enc.encode(pub[0], 16, 64)


def publicKey2Address(publicKey):
    """
        Compressed ECC public key hex to addresses using both versions
    """
    bAddress = base58Encode(hashlib.new('ripemd160', hashlib.sha256(publicKey.decode('hex')).digest()).digest(), 25,
        'B')
    sAddress = base58Encode(hashlib.new('ripemd160', hashlib.sha256(publicKey.decode('hex')).digest()).digest(), 63,
        'S')
    return bAddress, sAddress


def base58Encode(r160, magicbyte, prefix):
    """
        Base58 encoding w leading zero compact
    """
    from re import match as re_match

    inp_fmtd = chr(int(magicbyte if magicbyte < 255 else 255)) + r160
    leadingzbytes = len(re_match('^\x00*', inp_fmtd).group(0))
    checksum = hashlib.sha256(hashlib.sha256(inp_fmtd).digest()).digest()[:4]
    return str(prefix) * leadingzbytes + enc.encode(enc.decode(inp_fmtd + checksum, 256), 58, 0)
