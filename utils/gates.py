import nufhe
import numpy as np
from functools import reduce

devices = nufhe.find_devices(api="OpenCL")
ctx = nufhe.Context(device_id=devices[1])
secret_key, cloud_key = ctx.make_key_pair()


def full_adder(num1, num2, vm):
    u1 = vm.gate_nand(num1, num2)
    u2 = vm.gate_nand(num1, u1)
    u3 = vm.gate_nand(num2, u1)
    u4 = vm.gate_nand(u2, u3)
    print ("u4: ", ctx.decrypt(secret_key, u4))

    ## zero carry-bit
    s0 = u4
    c0_out = vm.gate_not(u1)

    ## one carry-bit
    s1 = vm.gate_not(u4)
    c1_out = vm.gate_nand(s1, u1)

    ## carry bit calculation
    s = []
    s.append(s0[0:1])
    # print (s0[0].shape)
    
    # c_in_dec = ctx.decrypt(secret_key, c_in)
    res1 = ctx.decrypt(secret_key, c0_out)
    res2 = ctx.decrypt(secret_key, s0)
    print ("s0: ", ctx.decrypt(secret_key, s0))
    print ("c0: ", ctx.decrypt(secret_key, c0_out))
    print ("s1: ", ctx.decrypt(secret_key, s1))
    print ("c1: ", ctx.decrypt(secret_key, c1_out))

    c_in = c0_out[0:1]
    for i in range(1, 8):
        res = vm.gate_mux(c_in, s1[i:i+1], s0[i:i+1])
        # print (res.shape)
        s.append(res)
        c_in = vm.gate_mux(c_in, c1_out[i:i+1], c0_out[i:i+1])

    # # s.append(c_in)
    # # print (len(s))
    s = nufhe.concatenate(s, axis=0)
    return s

## TODO: return value = true value - 1
def full_subtractor(num1, num2, vm):
    not_num2 = vm.gate_not(num2)
    diff = full_adder(num1, not_num2, vm)

    return diff


def comparator_4bits(A, B, vm):
    ## base block
    not_A = vm.gate_not(A)
    not_B = vm.gate_not(B)

    u1 = vm.gate_and(not_A, B)
    u2 = vm.gate_and(A, not_B)
    x = vm.gate_nor(u1, u2)

    ## common values
    and_x2_x3 = vm.gate_and(x[2:3], x[3:4])

    ## A == B
    is_equal = vm.gate_and(
        vm.gate_and(x[0:1], x[1:2]),
        and_x2_x3
    )

    ## A > B
    g2 = vm.gate_and(x[3:4], u2[2:3])
    g4 = vm.gate_and(
        and_x2_x3,
        u2[1:2]
    )
    g6 = vm.gate_and(
        and_x2_x3,
        vm.gate_and(u2[0:1], x[1:2])
    )

    is_greater = vm.gate_or(
        vm.gate_or(u2[3:4], g2),
        vm.gate_or(g4, g6)
    )

    ## A < B
    is_less = vm.gate_andny(
        is_equal,
        vm.gate_not(is_greater)
    )

    #######
    # res = ctx.decrypt(secret_key, is_less)
    # print (res)

    return is_equal, is_greater, is_less
    
def comparator_8bits(A, B, vm):
    equal_l, greater_l, less_l = comparator_4bits(A[0:4], B[0:4], vm)
    equal_g, greater_g, less_g = comparator_4bits(A[4:8], B[4:8], vm)

    is_equal = vm.gate_and(equal_g, equal_l)
    is_greater = vm.gate_or(
        greater_g,
        vm.gate_and(equal_g, greater_l)
    )

    is_less = is_less = vm.gate_andny(
        is_equal,
        vm.gate_not(is_greater)
    )

    return is_equal, is_greater, is_less

def swap_if_le(A, B, vm):
    eq, gt, lt = comparator_8bits(A, B, vm)
    le = vm.gate_or(eq, lt)

    C = vm.gate_mux(le, B, A)
    D = vm.gate_mux(le, A, B)

    return C, D

def swap_if_gt(A, B, vm):
    _, gt, _ = comparator_8bits(A, B, vm)

    C = vm.gate_mux(gt, B, A)
    D = vm.gate_mux(gt, A, B)

    return C, D

def sort(array, vm):
    for i in range(1, len(array)):
        for j in range(i, 0, -1):
            array[j - 1], array[j] = swap_if_gt(array[j - 1], array[j], vm)

if __name__ == "__main__":
    import random

    size = 8
    bits1 = np.unpackbits(np.array([227], dtype='>i1').view(np.uint8))[::-1]
    print (bits1)
    # print (np.array([258], dtype='>i2').view(np.uint8))
    bits2 = np.unpackbits(np.array([126], dtype='>i1').view(np.uint8))[::-1]

    ciphertext1 = ctx.encrypt(secret_key, bits1)
    ciphertext2 = ctx.encrypt(secret_key, bits2)

    # # # reference = [not (b1 and b2) for b1, b2 in zip(bits1, bits2)]

    vm = ctx.make_virtual_machine(cloud_key)
    # # comparator_8bits(ciphertext1, ciphertext2, vm)
    # C, D = swap_if_le(ciphertext1, ciphertext2, vm)

    const_100_bits = np.unpackbits(np.array([100], dtype='>i1').view(np.uint8))[::-1]
    const_100 = vm.gate_constant(const_100_bits)

    result = full_subtractor(ciphertext1, const_100, vm)
    result_bits = ctx.decrypt(secret_key, result)[::-1]
    # # C_bits = ctx.decrypt(secret_key, C)[::-1]
    # # C_value = np.packbits(C_bits, axis=0)

    # # D_bits = ctx.decrypt(secret_key, D)[::-1]
    # # D_value = np.packbits(D_bits, axis=0)

    # # print (C_value, D_value)
    value = np.packbits(result_bits, axis=0)
    print (result_bits)
    print (value.view('>i1'))

    ### test sorting
    # values = [32, 4, 15, 13, 11]
    # enc_values = []
    # for value in values:
    #     bits = np.unpackbits(np.array([value], dtype='>i2').view(np.uint8))[::-1][:8]
    #     ciphertext = ctx.encrypt(secret_key, bits)
    #     enc_values.append(ciphertext)

    # sort(enc_values, vm)
    # for enc_value in enc_values:
    #     bits = ctx.decrypt(secret_key, enc_value)[::-1]
    #     value = np.packbits(bits, axis=0)
    #     print (value)