#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import base64
from program import XmlEncryptor, XmlDecryptor

def decrypt_xml(input_path: str, output_path: str) -> bool:
    decryptor = XmlDecryptor()
    success = decryptor.decrypt_encrypted_xml(input_path, output_path)

    if success:
        pass
    else:
        sys.exit(1)

    return success

def encrypt_xml(input_path: str, output_path: str) -> bool:
    encryptor = XmlEncryptor()
    success = encryptor.encrypt_xml_file(input_path, output_path)

    if success:
        pass
    else:
        sys.exit(1)

    return success