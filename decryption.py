#!/usr/bin/env python3

import os
import shutil
import subprocess

INTERPRETER = "python" if os.name == "nt" else "python3"
PACKAGE_MANAGER = "pip" if os.name == "nt" else "pip3"

try:
    from tqdm import tqdm
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    try:
        subprocess.call(f"python -m {PACKAGE_MANAGER} install -r requirements.txt")
    except subprocess.CalledProcessError:
        print("One or more packages has failed to install!\n")
        exit()


def decrypt_file_aes(encrypted_file_path, key, output_dir, CHUNK_SIZE):
    try:
        with open(encrypted_file_path, "rb") as input_file:
            iv = input_file.read(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_file_path = f"{os.path.basename(encrypted_file_path)[:-4]}"

        file_size = os.path.getsize(encrypted_file_path) - 16  # Exclude I.V. size

        with open(encrypted_file_path, "rb") as input_file, open(
            decrypted_file_path, "wb"
        ) as output_file:
            input_file.seek(16)  # Skip 16-bit I.V.

            with tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Decrypting"
            ) as pbar:
                while True:
                    chunk = input_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    decrypted_chunk = decryptor.update(chunk)
                    output_file.write(decrypted_chunk)
                    pbar.update(len(chunk))

                final_chunk = decryptor.finalize()
                if final_chunk:
                    output_file.write(final_chunk)

        decrypted_file_name = os.path.basename(decrypted_file_path)
        decrypted_file_new_path = os.path.join(output_dir, decrypted_file_name)
        shutil.move(decrypted_file_path, decrypted_file_new_path)

        os.remove(encrypted_file_path)

        print(
            f"{encrypted_file_path} decrypted successfully. Decrypted file saved as {decrypted_file_new_path}"
        )
        return decrypted_file_new_path
    except Exception as e:
        print(f"Error occurred during decryption: {e}")
