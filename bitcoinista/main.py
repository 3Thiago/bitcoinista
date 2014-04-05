import pybitcointools as bc
import wallet, core
import getpass, sys, os

def main():

    clipboard_available = True
    try:
        import clipboard
    except ImportError:
        clipboard_available = False

    try:
        import console
        console.clear()
    except ImportError:
        pass
    
    cfg_file_name = 'bitcoinista_config.json'
    mainseed = ''
    pwhash = ''
    cfg_addr = ''
    
    # Read from config file if exists, create it otherwise
    if os.path.exists(cfg_file_name):
        mainseed, pwhash, cfg_addr = wallet.read_from_config_file(cfg_file_name)
    else:
        print 'Config file not found. Let us create a new one.'
        input = raw_input('Enter private key in WIF format, brainwallet passphrase (use at least 128 bits of entropy!) or press enter to create new random private key: ')
        if input == '':
            privkey = bc.random_key()
        

        pw = getpass.getpass('Enter AES encryption password: ')
        pwhash = wallet.hash_password(pw)
        pw2 = getpass.getpass('Enter password again: ')
        pw2hash = wallet.hash_password(pw2)
        if pwhash != pw2hash:
            raise Exception('Password does not match.')

        wallet.create_config_file(cfg_file_name, mainseed, pw)
        mainseed, pwhash, cfg_addr = wallet.read_from_config_file(cfg_file_name)
        print 'Config file created.'
        print 'Your new address is: {0}'.format(cfg_addr)
        return

    print 'Wallet address: ' + cfg_addr

    all_unspent = []
    try:
        all_unspent = bc.unspent(cfg_addr)
    except:
        try:
            all_unspent = bc.blockr_unspent(cfg_addr)
        except:
            raise Exception('Could not get address history.')
            
    balance = core.get_balance(all_unspent)
    if balance == 0:
        print 'Address has zero balance. Send some coins and try again.'
        return

    btc_balance = core.satoshi_to_btc(balance)

    print 'Wallet balance: {0} bitcoins ({1} satoshis)'.format(btc_balance,balance)
    print ' '

    destination_addr = None
    btc_amount = None

    # Get input from clipboard if available
    if clipboard_available:
        clipboard_input = clipboard.get()
        destination_addr, btc_amount = core.parse_bitcoin_uri(clipboard_input)

    if destination_addr == None:
        destination_addr = raw_input('Destination address (enter to abort)? ').strip()
        if destination_addr == '':
            print 'Transaction aborted.'
            return

    if btc_amount == None:
        btc_amount = float(raw_input('How many bitcoins to send? '))
        if btc_amount <= 0.0:
            raise Exception('Amount of bitcoins to send must be positive.')
        
    if not core.is_address_valid(destination_addr):
        raise Exception('Destination address {0} is invalid.'.format(destination_addr))

    amount_to_send = core.btc_to_satoshi(btc_amount)

    print 'Do you want to send'
    print '{0} bitcoins ({1} satoshis)'.format(btc_amount,amount_to_send)
    print 'to address'
    print destination_addr + '?'
    print 'To accept, enter your password. To abort, press enter.'
    print ' '

    pw = getpass.getpass()
    if pw == '\n':
        print 'Transaction aborted.'
        return

    hashedpw = wallet.hash_password(pw)

    while (hashedpw != pwhash):
        print 'Wrong password, try again.'
        if pw == '\n':
            print 'Transaction aborted.'
            return
        pw = getpass.getpass()
        hashedpw = wallet.hash_password(pw)

    prv = wallet.privkey_from_mainseed_pw(mainseed, pw)
    pw = ''
    addr = bc.privtoaddr(prv)

    # Check wallet address consistency
    if addr != cfg_addr:
        raise Exception('Address from config file does not match address from private key!')
        
    txfee = 10000
    btc_txfee = core.satoshi_to_btc(txfee)
    fee_input = raw_input('Transaction fee? (Enter for default {0} bitcoins)'.format(btc_txfee))
    if fee_input != '':
        btc_txfee = float(fee_input)
        txfee = core.btc_to_satoshi(btc_txfee)
        if btc_txfee < 0.0:
            raise Exception('Negative tx fee')
        elif btc_txfee >= 0.001:
            input = raw_input('Your tx fee ({0} bitcoins) is high. Are you sure? (y to continue, other key to abort)'.format(btc_txfee))
            if input != 'y':
                print 'Transaction aborted'
                return

    if(balance < amount_to_send + txfee):
        raise Exception("Insufficient funds to send {0} + {1} bitcoins.".format(btc_amount, btc_fee))
        
    tx_ins, tx_outs = core.simple_tx_inputs_outputs(addr, all_unspent, destination_addr, amount_to_send, txfee)

    print 'Creating and signing transaction...'
    tx = bc.mktx(tx_ins, tx_outs)

    print tx_ins
    print tx_outs
    
    for i in range(len(tx_ins)):
        tx = bc.sign(tx,i,prv)
    #print bc.deserialize(tx)

    print ' '
    print 'Sending transaction...'
    #bc.pushtx(tx)
    print 'Transaction sent.'
    print ' '

