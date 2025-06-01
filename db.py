from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shazam_db"]
collection = db["fingerprints"]

def add_to_db(hash_value, time_ms, song_name):
    collection.update_one(
        {"_id": hash_value},
        {"$push": {
            "matches": {
                "anchor_time_ms": time_ms,
                "song_name": song_name
            }
        }},
        upsert=True
    )

def query_by_hashes(hashes):
    collection.find()
    
def query_by_hash(hash_value):
    doc = collection.find_one({"_id": hash_value}, {"matches": 1, "_id": 0})
    if doc:
        return doc.get("matches", [])
    else:
        return []
