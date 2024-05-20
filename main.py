#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
import os
import time
import msvcrt
import sys
import shutil
from encryption import encrypt_file_aes, generate_random_word
from decryption import decrypt_file_aes


def enc(CHUNK_SIZE=1):
    try:
        root = tk.Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames()

        # location to save encrypted files
        output_dir = filedialog.askdirectory(title="Select output directory")

        root.destroy()

        key: bytes = os.urandom(32)

        # Save encryption key to a .txt file
        rand = generate_random_word()
        key_path = os.path.join(output_dir, f"{rand}cc{CHUNK_SIZE}.txt")
        with open(key_path, "wb") as file:
            file.write(key)

        for file_path in file_paths:
            encrypted_file_path = encrypt_file_aes(
                file_path, key, CHUNK_SIZE=CHUNK_SIZE, output_dir=output_dir
            )

            # Move encrypted file to specified output directory
            encrypted_file_name = os.path.basename(encrypted_file_path)
            encrypted_file_new_path = os.path.join(output_dir, encrypted_file_name)
            shutil.move(encrypted_file_path, encrypted_file_new_path)

        print("Encryption process completed. Encryption key saved as", key_path)
    except Exception as e:
        print(f"Error occurred during encryption: {e}")


def dec(CHUNK_SIZE):
    try:
        root = tk.Tk()
        root.withdraw()

        encrypted_file_paths = filedialog.askopenfilenames()

        #  location to save decrypted files
        output_dir = filedialog.askdirectory(title="Select output directory")

        root.destroy()

        key_file_path = filedialog.askopenfilename(defaultextension=".txt")

        with open(key_file_path, "rb") as key_file:
            key = key_file.read()

        for file_path in encrypted_file_paths:
            decrypted_file_path = decrypt_file_aes(
                file_path, key=key, output_dir=output_dir, CHUNK_SIZE=CHUNK_SIZE
            )

        print("Decryption process completed.")
        return decrypted_file_path
    except Exception as e:
        print(f"Error occurred during decryption: {e}")


def main():
    try:
        CHUNK_SIZE = int(input("Enter chunk size in megabytes: "))
        if CHUNK_SIZE < 0 or CHUNK_SIZE == 0:
            raise ValueError("Chunk size cannot be negative!")
        else:
            pass

        CHUNK_SIZE *= 1024 * 1024

        print(f"Using {CHUNK_SIZE} bytes as chunk size\n")

        user_input = int(
            input(
                "Enter '1' to encrypt file(s), '2' to decrypt file(s) and '3' to exit >>>  "
            )
        )
        if user_input == 1:
            enc(CHUNK_SIZE)
            print("Encryption complete! Press any key to exit.")
            if msvcrt.getch():
                sys.exit()
        elif user_input == 2:
            dec(CHUNK_SIZE)
            print("Decryption complete! Press any key to exit.")
            if msvcrt.getch():
                sys.exit()
        elif user_input == 3:
            print("Exiting program...")
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
            sys.exit()
        else:
            print("Invalid option!")
            time.sleep(0.5)
            os.system("cls" if os.name == "nt" else "clear")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
