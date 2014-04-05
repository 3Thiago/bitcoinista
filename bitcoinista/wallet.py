import pybitcointools as bc
import aes
import json

def create_wallet_file(filename, encr_privkey, addr):
    wal_dict = {}
    wal_dict['encr_privkey'] = encr_privkey
    wal_dict['address'] = addr
    wal_json = json.dumps(wal_dict)
    wal_file = open(filename, 'w')
    wal_file.write(wal_json)
    wal_file.close()

def read_from_wallet_file(filename):
    wal_file = open(filename, 'r')
    wal_json = wal_file.read()
    wal_file.close()
    wal_dict = json.loads(wal_json)
    encr_privkey = wal_dict['encr_privkey']
    wal_addr = wal_dict['address']
    return encr_privkey, wal_addr

def bin_hash_password(pw):
    return bc.bin_dbl_sha256(pw)

def encrypt_privkey(privkey, pw):
    bin_pwhash = bin_hash_password(pw)
    bin_encr_privkey = aes.encryptData(bin_pwhash, privkey)
    encr_privkey = bin_encr_privkey.encode('hex')
    
    return encr_privkey

def decrypt_privkey(encr_privkey, pw):

    bin_pwhash = bin_hash_password(pw)
    bin_encr_privkey = encr_privkey.decode('hex')
    privkey = aes.decryptData(bin_pwhash, bin_encr_privkey)

    return privkey

def privkey_from_user_input(input):
    method = ''
    privkey = ''
    if input == '':
        method = 'random'
        privkey = bc.random_key()
    else:
        format = ''
        try:
            format = bc.get_privkey_format(input)
        except:
            format = ''
        
        if format == 'wif':
            method = 'wif'
            privkey = bc.encode_privkey(input, 'hex')
        else:
            method = 'brain'
            privkey = bc.sha256(input)

    return privkey, method
