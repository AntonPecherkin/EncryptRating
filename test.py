from phe import paillier
import nufhe
import numpy as np
import requests
import json
import pickle
import base64
from utils import EncUInt8

size = 5
with open('phe_keys.pickle', 'rb') as f:
    public_key, private_key = pickle.load(f)


devices = nufhe.find_devices(api="OpenCL")
ctx = nufhe.Context(device_id=devices[1])

with open('fhe_keys.pickle', 'rb') as f:
    secret_key_bytes, cloud_key_bytes = pickle.load(f)
    secret_key = ctx.load_secret_key(secret_key_bytes)
    cloud_key = ctx.load_cloud_key(cloud_key_bytes)

vm = ctx.make_virtual_machine(cloud_key)

URL = 'http://127.0.0.1:5001'
headers = {'content-type': 'application/json'}


## publish rating
values = np.random.randint(1, 5, size=size, dtype=np.uint8)
values = [int(x) for x in values]
print (values)

values_enc = [public_key.encrypt(x) for x in values]
values_cipher = [str(x.ciphertext()) for x in values_enc]

body = json.dumps(values_cipher)
res = requests.post(URL + '/phe_votes', data=body, headers=headers)

# ## get rating
res = requests.get(URL + '/sorted_votes')
indecies = res.json()
print (indecies)

# votes_fhe = [base64.b64decode(x.encode('utf-8')) for x in values_cipher]
# votes_fhe = [EncUInt8.from_ciphertext(vm, ctx, x) for x in votes_fhe]
# values = [x.decrypt(secret_key, ctx) for x in votes_fhe]

# print (values)

# values_enc = [paillier.EncryptedNumber(public_key, int(x), 0) for x in values_cipher]
# values = [private_key.decrypt(x) for x in values_enc]

# print (values)