from passlib.hash import pbkdf2_sha512

password = input("password")
hash_password = pbkdf2_sha512.encrypt(password)
print(hash_password)
print(pbkdf2_sha512.verify("456456", hash_password))

