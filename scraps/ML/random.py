import hashlib

prehash = 'tsugi'
hashed = hashlib.sha1(bytes(prehash, "utf-8")).hexdigest()
print(hashed)