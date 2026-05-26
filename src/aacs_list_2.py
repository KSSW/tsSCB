# -*- coding: utf-8 -*-

def generate_hex_block(size):
    lines = []
    for i in range(0, size, 16):
        lines.append("00 " * 16)
    return "\n".join(lines)

hex_data_third_dict = {
    "MKB_RO.inf": generate_hex_block(0x500000)
}