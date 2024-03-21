from pyblake2 import blake2b

with open("names.txt", "r") as f:
    names = [name.lower() for name in f.read().splitlines()]

# Possible TODO is to make it input
my_name = "maurice"
digest = blake2b(digest_size=32)
digest.update(my_name.encode("utf-8"))
hash_of_my_name = digest.hexdigest()
print(hash_of_my_name)

counter = 0
for name in names:
    digest = blake2b(digest_size=32)
    digest.update(name.encode("utf-8"))
    hash_of_a_name = digest.hexdigest()
    if hash_of_a_name == hash_of_my_name and name != my_name:
        counter+=1
        print(f"Collision Found:\nName: {my_name} | Hash: {hash_of_my_name}\nName: {name} | Hash: {hash_of_a_name}")
print(counter)