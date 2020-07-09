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

signature = SIGNATURE
r_str, s_str = signature[0:64], signature[64:]

msg = msg_str.encode('utf-8')
user_id = user_id_str.encode('utf-8')
pub_key = pub_key_str.encode('utf-8')
pri_key = pri_key_str.encode('utf-8')
r = r_str.encode('utf-8')
s = s_str.encode('utf-8')

sm_lib.sm2_verify.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p]
verified = sm_lib.sm2_verify(msg, c_int(msg_len), user_id, c_int(user_id_len), pub_key, r, s)
print('verified: ' + str(True if verified == 0 else False))

# 只改动第一个字符，需要重新构建 r 和 s
invalid_signature = 'b75ecb05234b951fc521a5375c86afacc2757ab54a925896761f283613509d86c64162c86689c57c220639dd287502e9cf0ed98282fb5658c85bc1c625cd7462'

r_str, s_str = invalid_signature[0:64], invalid_signature[64:]
r = r_str.encode('utf-8')
s = s_str.encode('utf-8')

verified = sm_lib.sm2_verify(msg, c_int(msg_len), user_id, c_int(user_id_len), pub_key, r, s)
print('invalid signature verified: ' + str(True if verified == 0 else False))
