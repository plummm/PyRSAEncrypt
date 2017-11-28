# -*- coding:utf-8 -*-
import os
import sys
import rsa
import hashlib
import shutil
import rsa.randnum
from Crypto.Cipher import AES
from Crypto import Random

file_headers = b'cnss'


def scan_files(directory, prefix=None, postfix='.py'):   #扫描文件夹下的py文件，directory为目录，prefix为前缀，postfix为后缀
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))
    return files_list


def encrypt_files(filename, output_directory, rsa_key):
    py_file = open(filename, 'r')
    file_data = py_file.read().encode()
    file_data += (16 - len(file_data) % 16) * ' '

    #aes encrypt
    aes_key = rsa.randnum.read_random_bits(128)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    encripted_data = iv + cipher.encrypt(file_data)
    #print (encripted_data)
    encripted_aes_key = rsa.encrypt(aes_key, rsa_key)
    out_put_file = open(output_directory, 'wb')
    total_data = encripted_aes_key + encripted_data
    output_data = file_headers + total_data
    out_put_file.write(output_data)
    py_file.close()
    out_put_file.close()


def decrypt_files(filename, output_directory, rsa_key):
    py_file = open(filename, 'rb')
    file_data = py_file.read()
    aes_key = file_data[36:164]
    aes_iv = file_data[164:180]
    data = file_data[180:]
    decrypted_aes_key = rsa.decrypt(aes_key, rsa_key)
    cipher = AES.new(decrypted_aes_key, AES.MODE_CBC, aes_iv)
    decrypted_date = cipher.decrypt(data).decode('utf-8')

    out_put_file = open(output_directory, 'wb')
    out_put_file.write(decrypted_date)
    py_file.close()
    out_put_file.close()


def main(argv):
    if len(argv) != 4 and len(argv) != 2:
        print('usage [<input_folder_name> <output_folder_name> <rsa_key_file>] [-generate]')
        print('      ')
        return
    if len(argv) == 4:
        input_floder_name = '/'+argv[1]
        output_floder_name = '/'+argv[2]
        py_file_list = scan_files(os.getcwd()+input_floder_name)

        copy_dir(os.getcwd()+input_floder_name, os.getcwd() + output_floder_name)

        #try:
        key_file = open(os.getcwd()+'/'+argv[3],'r')
        rsa_key = rsa.PublicKey.load_pkcs1(key_file.read().encode())
        #rsa_key = rsa.PrivateKey.load_pkcs1(key_file.read().encode())
        #except FileNotFoundError:
        #    print('can\'t find key file')
        #    return
        for file_name in py_file_list:
            encrypt_files(file_name, file_name.replace(input_floder_name,output_floder_name), rsa_key)
            print('encrypt file '+ file_name + ' success')
    if len(argv) == 2:
        if argv[1] == '-generate':
            generate_key()


def generate_key():
    # 生成密钥
    (pubkey, privkey) = rsa.newkeys(1024)
    # 保存密钥
    with open('public.pem', 'w+') as f:
        f.write(pubkey.save_pkcs1().decode())
        f.close()
    with open('private.pem', 'w+') as f:
        f.write(privkey.save_pkcs1().decode())
        f.close()


def copy_dir(old, new):
    try:
        shutil.copytree(old, new)
    except FileExistsError:
        shutil.rmtree(new)
        shutil.copytree(old, new)
    return

if __name__ == '__main__':
    # generate_key()

    main(sys.argv)