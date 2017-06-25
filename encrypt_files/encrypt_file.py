# -*- coding:utf-8 -*-
import os
import sys
import rsa
import hashlib

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
    encripted_data = rsa.encrypt(file_data, rsa_key)
    out_put_file = open(output_directory, 'wb')
    encripted_data = file_headers + bytes(hashlib.md5(file_data).hexdigest(),encoding='ascii') + encripted_data
    out_put_file.write(encripted_data)
    py_file.close()
    out_put_file.close()


def decrypt_files(filename, output_directory, rsa_key):
    py_file = open(filename, 'rb')
    file_data = py_file.read()
    encripted_data = rsa.decrypt(file_data, rsa_key)
    out_put_file = open(output_directory, 'wb')
    out_put_file.write(encripted_data)
    py_file.close()
    out_put_file.close()


def main(argv):
    if len(argv) != 4:
        print('usage <input_floder_name> <output_floder_name> <rsa_key_file>')
        return
    input_floder_name = '/'+argv[1]
    output_floder_name = '/'+argv[2]
    py_file_list = scan_files(os.getcwd()+input_floder_name)
    try:
        os.makedirs(os.getcwd()+output_floder_name)
    except FileExistsError:
        pass
    try:
        key_file = open(os.getcwd()+'/'+argv[3],'r')
        rsa_key = rsa.PublicKey.load_pkcs1(key_file.read().encode())
    except FileNotFoundError:
        print('can\'t find key file')
        return
    for file_name in py_file_list:
        encrypt_files(file_name, file_name.replace(input_floder_name,output_floder_name), rsa_key)
        print('encrypt file '+ file_name + ' success')

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

if __name__ == '__main__':
    # generate_key()
    main(sys.argv)