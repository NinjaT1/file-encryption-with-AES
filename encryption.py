#!/usr/bin/env python3

import os
import shutil
import string
import random
import subprocess

try:
    from tqdm import tqdm
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    try:
        subprocess.call("python -m pip install -r requirements.txt")
    except subprocess.CalledProcessError:
        print("One or more packages has failed to install!\n")
        exit()


def encrypt_file_aes(file_path, key, output_dir, CHUNK_SIZE):
    try:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        og_file = f"{os.path.basename(file_path)}"
        encrypted_file_path = f"{os.path.basename(file_path)}.enc"

        file_size = os.path.getsize(file_path)

        with open(file_path, "rb") as input_file, open(
            encrypted_file_path, "wb"
        ) as output_file:
            output_file.write(iv)
            with tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Encrypting"
            ) as pbar:
                while True:
                    chunk = input_file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    padded_chunk = padder.update(chunk)
                    encrypted_chunk = encryptor.update(padded_chunk)
                    output_file.write(encrypted_chunk)
                    pbar.update(len(chunk))

                final_chunk = padder.finalize()
                if final_chunk:
                    final_encrypted_chunk = (
                        encryptor.update(final_chunk) + encryptor.finalize()
                    )
                    output_file.write(final_encrypted_chunk)

        encrypted_file_name = os.path.basename(encrypted_file_path)
        encrypted_file_new_path = os.path.join(output_dir, encrypted_file_name)
        shutil.move(encrypted_file_path, encrypted_file_new_path)

        os.remove(file_path)

        print(
            f"{og_file} encrypted successfully. Encrypted file saved as {encrypted_file_new_path}"
        )
        return encrypted_file_new_path
    except Exception as e:
        print(f"Error occurred during encryption: {e}")


def generate_random_key():
    return os.urandom(32)  # 256-bit key


def generate_random_word(length=5):
    return "".join(random.choices(string.ascii_lowercase, k=length))
