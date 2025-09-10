from cryptography.fernet import Fernet

key = Fernet.generate_key()
Cipher_suite = Fernet(key)
token = Cipher_suite.encrypt(b"This is a really secret message! Not for sharing.")
print(token)

decrypted = Cipher_suite.decrypt(token)

# Used for communication between server and client
print("Decrypted token = ", decrypted)

# Used for presentation (Gets rid of the b' ')
print(decrypted.decode('utf-8'))