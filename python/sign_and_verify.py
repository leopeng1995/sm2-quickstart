import os

from ctypes import *
from constants import PUBLIC_KEY, PRIVATE_KEY, SIGNATURE, MESSAGE


so_file = os.path.join(os.getcwd(), '..', 'SM2-signature-creation-and-verification', 'sm_lib.so')
sm_lib = CDLL(so_file)

msg_str = MESSAGE
msg_len = len(msg_str)
user_id_str = '1234567812345678'
user_id_len = len(user_id_str)

pub_key_str = PUBLIC_KEY
pri_key_str = PRIVATE_KEY

msg = msg_str.encode('utf-8')
user_id = user_id_str.encode('utf-8')
pub_key = pub_key_str.encode('utf-8')
pri_key = pri_key_str.encode('utf-8')

sm_lib.sm2_sign.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p]
# 注：如果直接不适用 c_void_p，而使用原来的返回值来释放内存会报异常。
# https://stackoverflow.com/questions/13445568/python-ctypes-how-to-free-memory-getting-invalid-pointer-error
# sm_lib.sm2_sign.restype = c_char_p
sm_lib.sm2_sign.restype = c_void_p
sig = sm_lib.sm2_sign(msg, c_int(msg_len), user_id, c_int(user_id_len), pub_key, pri_key)

if sig:
    sig_val = cast(sig, c_char_p).value
    sig_str = sig_val.decode('utf-8')
    print('signature: ' + sig_str)
    r_str, s_str = sig_str[0:64], sig_str[64:]

    r = r_str.encode('utf-8')
    s = s_str.encode('utf-8')

    sm_lib.sm2_verify.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p]
    verified = sm_lib.sm2_verify(msg, c_int(msg_len), user_id, c_int(user_id_len), pub_key, r, s)
    print('verified: ' + str(True if verified == 0 else False))

    sm_lib.sm2_free.argtypes = [c_char_p]

    sig = cast(sig, c_char_p)
    # 注意要释放掉 C 端创建的内存，否则会溢出。
    sm_lib.sm2_free(sig)
