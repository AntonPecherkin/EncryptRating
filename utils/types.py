import nufhe
import numpy as np
from .gates import full_adder, full_subtractor

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

    def __add__(self, other):
        res = full_adder(self.ciphertext, other.ciphertext, self.vm)
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