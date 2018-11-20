import plyvel
import bson
db = plyvel.DB('./tweets', create_if_missing=True)

# for key, value in db:
#     print(key.decode("utf-8"))
#     print(bson.loads(value))

print(sum(1 for _ in db))