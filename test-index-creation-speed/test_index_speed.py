import pymongo
import random
import string
import time
from faker import Faker

fake = Faker()
collection_size = [100, 1000, 10000, 100000, 1000000]
field_to_index = 'address'
string_length = 3
db = pymongo.MongoClient('mongodb://127.0.0.1:27017')['test']

def random_arr(collection_size):
    master_arr = []
    for n in range(collection_size):
        a = {
            "text": fake.text(),
            "address": fake.address(),
            "phone": fake.phone_number()
        }
        master_arr.append(a)

    return master_arr


def tail_oplog():
    oplog = db.local.oplog.rs
    first = oplog.find().sort('$natural', pymongo.ASCENDING).limit(-1).next()
    ts = first['ts']

    while True:
        cursor = oplog.find({'ts': {'$gt': ts}}, cursor_type=pymongo.CursorType.TAILABLE_AWAIT, oplog_replay=True)

        while cursor.alive:
            for doc in cursor:
                if 'msg' in doc['o']:
                    if doc['o']['msg'] == 'Creating indexes. Coll: test.test0':
                        print(doc)


def main(collection_size):
    # clear collection
    print("clearing collection")
    db.test.delete_many({})

    # clear indexes
    print("dropping indexes")
    db.test.drop_indexes()

    # create
    print("creating array")
    arr_to_insert = random_arr(collection_size)

    # insert
    print("inserting")
    db.test.insert_many(arr_to_insert)

    # time index creation
    # p = Process(target=tail_oplog)
    print("creating indexes")
    start_time = time.time()
    db.test.create_index(field_to_index)
    print(f"index creation of size: {collection_size} and index length: {string_length} took {time.time() - start_time} seconds")



if __name__ == "__main__":
    for i in collection_size_array:
        main(collection_size=i)
