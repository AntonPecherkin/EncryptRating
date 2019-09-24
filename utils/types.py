import nufhe
import numpy as np
from .gates import full_adder, full_subtractor, swap_if_le, swap_if

class EncUInt8(object):
    def __init__(self, ciphertext, vm):
        self.vm = vm
        self.ciphertext = ciphertext

    @classmethod
    def from_scalar(cls, vm, scalar):
        bits = np.unpackbits(np.array([scalar], dtype='>i1').view(np.uint8))[::-1]
        ciphertext = vm.gate_constant(bits)
        return cls(ciphertext, vm)

    @classmethod
    def from_uint8(cls, vm, sk, ctx, value):
        bits = np.unpackbits(np.array([value], dtype='>i1').view(np.uint8))[::-1]
        ciphertext = ctx.encrypt(sk, bits)
        return cls(ciphertext, vm)

    @classmethod
    def from_ciphertext(cls, vm, ctx, cipher_bytes):
        print (type(cipher_bytes))

        ciphertext = ctx.load_ciphertext(cipher_bytes)
        return cls(ciphertext, vm)

    def __add__(self, other):
        res = full_adder(self.ciphertext, other.ciphertext, self.vm)
        # print (res)
        
        return EncUInt8(res, self.vm)

    def __sub__(self, other):
        res = full_subtractor(self.ciphertext, other.ciphertext, self.vm)

        return EncUInt8(res, self.vm)

    def decrypt(self, sk, ctx):
        result_bits = ctx.decrypt(sk, self.ciphertext)[::-1]
        value = np.packbits(result_bits, axis=0)
        # print (value.view('>i1'))

        return value

    def dumps(self):
        return self.ciphertext.dumps()

def sort_encrypted(array, indecies, vm):
    for i in range(1, len(array)):
        for j in range(i, 0, -1):
            print (type(array[j]))
            array[j - 1].ciphertext, array[j].ciphertext, le  = swap_if_le(array[j - 1].ciphertext, array[j].ciphertext, vm)
            indecies[j - 1].ciphertext, indecies[j].ciphertext = swap_if(indecies[j - 1].ciphertext, indecies[j].ciphertext, le, vm)

if __name__ == "__main__":
    size = 5

    devices = nufhe.find_devices(api="OpenCL")
    ctx = nufhe.Context(device_id=devices[1])
    secret_key, cloud_key = ctx.make_key_pair()
    vm = ctx.make_virtual_machine(cloud_key)


    values_x = np.random.randint(1, 5, size=size, dtype=np.uint8)
    # values = [int(x) for x in values]
    print (values_x)

    values_x_enc = [EncUInt8.from_uint8(vm, secret_key, ctx, x) for x in values_x]
    values_x_enc = np.array(values_x_enc)

    # values_y = np.random.randint(1, 5, size=size, dtype=np.uint8)
    # # values = [int(x) for x in values]
    # print (values_y)

    # values_y_enc = [EncUInt8.from_uint8(vm, secret_key, ctx, x) for x in values_y]
    # values_y_enc = np.array(values_y_enc)

    # res = values_x_enc[0] + values_y_enc[0]

    res = values_x_enc# + values_y_enc

    sum_res = [x.decrypt(secret_key, ctx) for x in res]
    print (sum_res)

    ### test sorting
    indecies = [EncUInt8.from_scalar(vm, x) for x in range(size)]

    cipher_to_idx = {}
    for i in range(size):
        cipher_to_idx[indecies[i].dumps()] = i

    sort_encrypted(res, indecies, vm)

    result = [cipher_to_idx[idx.dumps()] for idx in indecies]
    print (result)