import json
import pybitcointools as bc

def read_from_config_file(filename):
    cfg_file = open(filename, 'r')
    cfg_json = cfg_file.read()
    cfg_file.close()
    cfg_dict = json.loads(cfg_json)
    mainseed = cfg_dict['mainseed']
    pwhash = cfg_dict['pwhash']
    cfg_addr = cfg_dict['address']
    return mainseed, pwhash, cfg_addr

def hash_password(pw):
    return bc.sha256(pw)

def privkey_from_mainseed_pw(mainseed, pw):
    return bc.sha256(mainseed + pw)
    
def create_config_file(filename, mainseed, pw):
    pwhash = hash_password(pw)
    prv = privkey_from_mainseed_pw(mainseed, pw)
    addr = bc.privtoaddr(prv)
    cfg_dict = {}
    cfg_dict['mainseed'] = mainseed
    cfg_dict['pwhash'] = pwhash
    cfg_dict['address'] = addr
    cfg_json = json.dumps(cfg_dict)
    cfg_file = open(filename, 'w')
    cfg_file.write(cfg_json)
    cfg_file.close()


