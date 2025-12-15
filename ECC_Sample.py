# pip install eciespy
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii

privKey = generate_eth_key()
privKeyHex = privKey.to_hex()
pubKeyHex = privKey.public_key.to_hex()
print("Encryption public key:", pubKeyHex, type(pubKeyHex))
print("Decryption private key:", privKeyHex, type(privKeyHex))

plaintext = b'Some plaintext for encryption'
print("Plaintext:", plaintext,type(plaintext))

encrypted = encrypt(pubKeyHex, plaintext)
cipher = binascii.hexlify(encrypted)
print("Encrypted:", binascii.hexlify(encrypted), type(cipher))

decrypted = decrypt(privKeyHex, encrypted)
print("Decrypted:", decrypted)

pub = '0x234ee8cb6f0ca19a016ddeb5c3acde5a627aa553e18f070dbbadf86b138567f4178b915213bf1f80ddae7b4ee82b5ac675611d6850cc6c59c4a85fcbe86a636f'
priv = '0xf6522fa7d69fe07d0ecfd9c4307319b068637dc3d98cd42da03972ba21f521a3'
c= b"\x04\xa0\xafk\x94\xb8\xef\xd7\xcb|k\xc4\xede\xff\x0e\xf8fK\xb6\xb0\xa0\x89r\xff\xfan\x8a\xdc\xbe\x90Gx\x18n\xbe[\x87'\xde\xc9=2.I6Jv\xa9d\xc4\xc8\x04B5\xb40@\x06E\xb6\x9b\xd2\xa6:\xfb7PJA\xf2\x89;%o\xcf\x10_Yqa\x81\x11}2\n\x80W\xa16\x14p\x99&@\xd6Xk\x87\x16\x0b\x17\x92\xf3\xce\xf4YL\xd4\xc2`;\x99\xd7Z>\x00(\xc2X`X:|*\xd5\x8b\xfb\xfb`\x88\xbb\xfdM1\x13\x08\xf3\xe7"
d = decrypt(priv, c)
print("Decrypted:", d)


