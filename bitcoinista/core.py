import urlparse
import pybitcointools as bc

def get_balance(unspent):
    balance = 0
    for u in unspent:
        balance += u['value']
    
    return balance

def satoshi_to_btc(val):
    return (float(val) / 10**8)

def btc_to_satoshi(val):
    return int(val * 10**8 + 0.5)

# Return the address and btc_amount from the
# parsed uri_string. If either of address
# or amount is not found that particular
# return value is None.
def parse_bitcoin_uri(uri_string):
    parsed = urlparse.urlparse(uri_string)
    if parsed.scheme == 'bitcoin':
        addr = parsed.path
        queries = urlparse.parse_qs(parsed.query)
        if 'amount' not in queries:
            btc_amount = None
        elif len(queries['amount']) == 1:
            btc_amount = float(queries['amount'][0])
        else:
            btc_amount = None
        return addr, btc_amount
    else:
        return None, None

# Returns valid for both scriptpubkey,
# scripthash and stealth addresses
def is_address_valid(addr, on_testnet=False):
    
    # Check if scripthash,
    # pubkey or stealth address
    if on_testnet:
        if addr[0] == '2':
            magic_byte = 192
        elif addr[0] == 'm' or addr[0] == 'n':
            magic_byte = 111
        elif addr[0] == 'w':
            magic_byte = 43
        else:
            return False
    else:
        if addr[0] == '3':
            magic_byte = 5
        elif addr[0] == '1':
            magic_byte = 0
        elif addr[0] == 'v':
            magic_byte = 42
        else:
            return False
        
    addr_valid = True
    try:
        bin_addr = bc.b58check_to_bin(addr)
        if bc.bin_to_b58check(bin_addr, magic_byte) != addr:
            addr_valid = False
    except:
        addr_valid = False

    return addr_valid

def simple_tx_inputs_outputs(from_addr, from_addr_unspent, to_addr, amount_to_send, txfee):

    selected_unspent = bc.select(from_addr_unspent, amount_to_send+txfee)
    selected_unspent_bal = get_balance(selected_unspent)
    changeval = selected_unspent_bal - amount_to_send - txfee
    if to_addr[0] == 'v' or to_addr[0] == 'w':
        # stealth
        ephem_privkey = bc.random_key()
        nonce = int(bc.random_key()[:8],16)
        if to_addr[0] == 'v':
            network = 'btc'
        else:
            network = 'testnet'
            
        tx_outs = bc.mk_stealth_tx_outputs(to_addr, amount_to_send, ephem_privkey, nonce, network)
    else: 
        tx_outs = [{'value' : amount_to_send, 'address' : to_addr}]
        
    if changeval > 0:
        tx_outs.append({'value' : changeval, 'address' : from_addr})

    return selected_unspent, tx_outs

