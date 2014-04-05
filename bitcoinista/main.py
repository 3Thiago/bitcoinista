import pybitcointools as bc
import wallet, core
import getpass, sys, os

def get_demo_unspent():
    unspent = [{'output': '2818b4de824faa41539c4501cc68912e2da07a050b407024c56f8e622cc208c4:1', 'value': 10000000},
               {'output': '58df9f2348323f46706d84e83b31d685e88100e21feab3a6bd91859670199c0a:1', 'value': 50000000},
               {'output': '09604cfd3e2bfdef31e1404c93249023955634cd8686f02adaa7694ca6cafdea:3', 'value': 20000000}
               ]

    return unspent

def main(demo_mode=False):

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
    
    wal_file_name = 'bitcoinista_wallet.json'
    wal_addr = ''
    
    # Read from config file if exists, create it otherwise
    if os.path.exists(wal_file_name):
        encr_privkey, wal_addr = wallet.read_from_wallet_file(wal_file_name)
    else:
        print 'Config file not found. Let us create a new one.'
        input = raw_input('Enter private key in WIF format, brainwallet passphrase (use at least 128 bits of entropy!) or press enter to create new random private key: ')

        privkey, method = wallet.privkey_from_user_input(input)
        wal_addr = bc.privtoaddr(privkey)

        pw = getpass.getpass('Enter AES encryption password: ')
        pw2 = getpass.getpass('Enter password again: ')
        if pw != pw2:
            raise Exception('Passwords does not match.')

        encr_privkey = wallet.encrypt_privkey(privkey, pw)
        wallet.create_wallet_file(wal_file_name, encr_privkey, wal_addr)
        
        # Read back from wallet to ensure consistency
        encr_privkey2, wal_addr2 = wallet.read_from_wallet_file(wal_file_name)
        privkey2 = wallet.decrypt_privkey(encr_privkey2, pw)
        
        if encr_privkey2 != encr_privkey or wal_addr2 != wal_addr:
            raise Exception('Inconsistency in reading from/writing to wallet!')

        if privkey2 != privkey:
            raise Exception('Inconsistency in encrypting/decrypting private key!')

        wif_privkey = bc.encode_privkey(privkey2, 'wif')

        if method == 'wif':
            print 'Private key imported. Your input was'
            print input
            print 'and the saved private key is'
            print wif_privkey
            print 'Make sure they are the same!'
        elif method == 'brain':
            print 'Brain wallet created from string'
            print input
            print 'with saved private key'
            print wif_privkey
        elif method == 'random':
            print 'Random private key created. Saved private key is'
            print wif_privkey

        print ' '
        print 'Your address is: {0}'.format(wal_addr)
        return

    print 'Wallet address: ' + wal_addr

    all_unspent = []
    if demo_mode:
        all_unspent = get_demo_unspent()
    else:
        try:
            all_unspent = bc.unspent(wal_addr)
        except:
            try:
                all_unspent = bc.blockr_unspent(wal_addr)
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

    prv = wallet.decrypt_privkey(encr_privkey, pw)
    addr = bc.privtoaddr(prv)

    # Check wallet address consistency
    if addr != wal_addr:
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

    for i in range(len(tx_ins)):
        tx = bc.sign(tx,i,prv)

    if demo_mode:
        print 'Total unspent outputs before transaction: ' + str(all_unspent)
        print ' '
        print 'Transaction inputs: ' + str(tx_ins)
        print ' '
        print 'Transaction outputs: ' + str(tx_outs)
        print ' '
        print 'Deserialized final transaction: ' + str(bc.deserialize(tx))
        print ' '
    else:
        print ' '
        print 'Sending transaction...'

        try:
            bc.pushtx(tx)
        except:
            bc.eligius_pushtx(tx)

        print 'Transaction sent.'
    print ' '

    return
