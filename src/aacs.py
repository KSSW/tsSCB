#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from aacs_list_0 import hex_data_one_dict
from aacs_list_1 import hex_data_two_dict
from aacs_list_2 import hex_data_third_dict
from aacs_list_3 import hex_data_fourth_dict
from aacs_list_4 import cer
from aacs_list_5 import xsd

def hxd_bin(mp):

    AACS = os.path.join(mp, "Output", "MUX", "BDROM", "DB", "AACS")
    AACS_DUPLICATE = os.path.join(mp, "Output", "MUX", "BDROM", "DB", "AACS", "DUPLICATE")
    CERTIFICATE = os.path.join(mp, "Output", "MUX", "BDROM", "DB", "CERTIFICATE")
    CERTIFICATE_BACKUP = os.path.join(mp, "Output", "MUX", "BDROM", "DB", "CERTIFICATE", "BACKUP")

    XSD = os.path.join(mp, "Output", "MUX", "BDROM")
        
    os.makedirs(AACS, exist_ok=True)
    os.makedirs(AACS_DUPLICATE, exist_ok=True)
    os.makedirs(CERTIFICATE, exist_ok=True)
    os.makedirs(CERTIFICATE_BACKUP, exist_ok=True)

    merged_dict = {**hex_data_one_dict, **hex_data_two_dict, **hex_data_third_dict, **hex_data_fourth_dict}

    for filename, hex_str in merged_dict.items():
        clean_hex = hex_str.replace('\n', ' ').replace('\r', ' ').strip()
        hex_bytes = bytes.fromhex(clean_hex)

        aacs_path = os.path.join(AACS, filename)

        if os.path.exists(aacs_path):
            with open(aacs_path, 'rb') as existing_file:
                existing_content = existing_file.read()
                if existing_content == hex_bytes:
                    continue
                else:
                    pass

        aacs_path = os.path.join(AACS, filename)
        with open(aacs_path, 'wb') as f:
            f.write(hex_bytes)

        aacs_dup_path = os.path.join(AACS_DUPLICATE, filename)

        if os.path.exists(aacs_dup_path):
            with open(aacs_dup_path, 'rb') as existing_file:
                existing_content = existing_file.read()
                if existing_content == hex_bytes:
                    continue
                else:
                    pass

        aacs_dup_path = os.path.join(AACS_DUPLICATE, filename)
        with open(aacs_dup_path, 'wb') as f:
            f.write(hex_bytes)

    for filename, hex_str in cer.items():
        clean_hex = hex_str.replace('\n', ' ').replace('\r', ' ').strip()
        hex_bytes = bytes.fromhex(clean_hex)

        cer_path = os.path.join(CERTIFICATE, filename)

        if os.path.exists(cer_path):
            with open(cer_path, 'rb') as existing_file:
                existing_content = existing_file.read()
                if existing_content == hex_bytes:
                    continue
                else:
                    pass

        cer_path = os.path.join(CERTIFICATE, filename)
        with open(cer_path, 'wb') as f:
            f.write(hex_bytes)

        cer_dup_path = os.path.join(CERTIFICATE_BACKUP, filename)

        if os.path.exists(cer_dup_path):
            with open(cer_dup_path, 'rb') as existing_file:
                existing_content = existing_file.read()
                if existing_content == hex_bytes:
                    continue
                else:
                    pass

        cer_dup_path = os.path.join(CERTIFICATE_BACKUP, filename)
        with open(cer_dup_path, 'wb') as f:
            f.write(hex_bytes)

    for filename, hex_str in xsd.items():
        clean_hex = hex_str.replace('\n', ' ').replace('\r', ' ').strip()
        hex_bytes = bytes.fromhex(clean_hex)

        xsd_path = os.path.join(XSD, filename)

        if os.path.exists(xsd_path):
            with open(xsd_path, 'rb') as existing_file:
                existing_content = existing_file.read()
                if existing_content == hex_bytes:
                    continue
                else:
                    pass

        xsd_path = os.path.join(XSD, filename)
        with open(xsd_path, 'wb') as f:
            f.write(hex_bytes)