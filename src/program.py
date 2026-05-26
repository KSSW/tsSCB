#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

dlkey = bytes([
    0x50, 0x63, 0x6A, 0x51,
    0x47, 0x45, 0x48, 0x46,
    0x70, 0x6F, 0x72, 0x71,
    0x67, 0x65, 0x68, 0x66
])
magic_header = bytes([162, 179, 196, 230])

class XmlEncryptor:
    def encrypt_xml_file(self, input_path, output_path):
        result = True
        try:
            with open(input_path, 'rb') as f:
                xml_data = f.read()

            if xml_data.startswith(magic_header):
                print("File is encrypted.")
                return True

            cipher = AES.new(dlkey, AES.MODE_CBC, iv=dlkey)
            padded_data = pad(xml_data, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)

            with open(output_path, 'wb') as out_file:
                out_file.write(magic_header)
                out_file.write(encrypted_data)

        except Exception as e:
            print(f"Encryption failed: {e}")
            result = False
        return result

class XmlDecryptor:
    def decrypt_encrypted_xml(self, encrypted_xml_path, output_xml_path):
        result = True
        try:
            with open(encrypted_xml_path, 'rb') as file_stream:
                header = file_stream.read(4)
                if header != magic_header:
                    raise ValueError("Not a legal encrypted file.")

                encrypted_data = file_stream.read()

                cipher = AES.new(dlkey, AES.MODE_CBC, iv=dlkey)
                decrypted_data = cipher.decrypt(encrypted_data)
                unpadded = unpad(decrypted_data, AES.block_size)

                with open(output_xml_path, 'wb') as output_file:
                    output_file.write(unpadded)

        except Exception as ex:
            print(f"Decryption failed: {str(ex)}")
            result = False
        return result
