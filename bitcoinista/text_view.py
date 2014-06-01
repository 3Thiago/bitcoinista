import getpass


class TextView:
    
    def __init__(self):
        pass
            
    def draw_splash_screen(self, user_mode):
        try:
            import console
            console.clear()
        except ImportError:
            pass
        
        if user_mode == 'mainnet':
            print '*****************'
            print '** BITCOINISTA **'
            print '*****************'
            print ''
        elif user_mode == 'demo':
            print '*****************************'
            print '** BITCOINISTA (DEMO MODE) **'
            print '*****************************'
            print ''
        else:
            raise Exception('Unsupported user mode ' + user_mode)   
               
    def draw_address_and_balance(self, addr, btc_balance):
        print '** Address and Balance **'
        print addr
        print '{0} BTC'.format(btc_balance)
        print ' '

    def draw_zero_balance(self):
        print 'Address has zero balance. Please send some coins.'
        print 'Thank you for using Bitcoinista!'
             
    def draw_insufficient_balance(self):
        print 'Insufficient balance!'

    def draw_new_transaction(self):
        print '** New Transaction **' 
        
    def request_create_wallet_method(self):
        print 'Wallet file not found. Let us create a new one.'
        print 'Enter method for generating private key:'
        print '* (r)andom key'
        print '* (b)rainwallet passphrase'
        print '* Imported (p)rivate key'
        
        input = ''
        while input != 'r' and input != 'b' and input != 'p':
            input = raw_input('Select method (r/b/p):')
        method = ''
        if input == 'r':
            method = 'random'
        elif input == 'b':
            method = 'brain'
        elif input == 'p':
            method = 'wif'
        
        return method
        
    def request_create_wallet_input(self, method):
        
        input = ''
        if method == 'wif':
            input = raw_input('Enter private key in WIF format:')
        elif method == 'brain':
            input = raw_input('Enter brainwallet passphrase (use at least 128 bits of entropy!):')
        else:
            raise Exception('Unsupported method type for input request.')
        
        return input
    
    def request_wallet_pw(self, ask_twice=False):
        pw = getpass.getpass('Enter AES encryption password: ')
        if ask_twice:
            pw2 = getpass.getpass('Enter password again: ')
            if pw != pw2:
                print 'Passwords do not match!'
                return None
            elif pw == '' or pw == '\n':
                print 'Empty password!'
                return None
        
        return pw

    def draw_create_wallet_result(self, method, input, wif_privkey, addr):
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
        else:
            raise Exception('Unsupported method: {0}.'.format(method))
        
        print ''
        print 'Your address is {0}.'.format(addr)

        return
        
    def request_destination_address(self):
        destination_addr = raw_input('Destination (enter to abort): ').strip()
        return destination_addr

    def request_send_amount(self):
        btc_amount = raw_input('Amount(BTC): ')
        return btc_amount

    def draw_destination_address(self, dest_addr):
        print 'Destination: ' + dest_addr
        
    def draw_send_amount(self, btc_amount):        
        print 'Amount(BTC): ' + str(btc_amount)
        
    def request_txfee(self, default_btc_txfee):
        text = 'Transaction fee (enter for default {0} BTC): '.format(default_btc_txfee)
        input = raw_input(text)
        if input == '':
            btc_txfee = default_btc_txfee
        else:
             btc_txfee = float(input)

        return btc_txfee

    def draw_txfee_warning(self, msg, btc_txfee):
        input = ''
        if msg == 'LARGE':
            input = raw_input('Your TX fee ({0} BTC) is high. Are you sure? (y to continue, other key to abort)'.format(btc_txfee))
        elif msg == 'ZERO':
            input = raw_input('Zero transaction fee. Are you sure? (y to continue, other key to abort)')     
        else:
            raise Exception('Unsupported message ' + msg)
            
        return input

    def draw_abort(self):
        print 'Transaction aborted.'

    def draw_demo_tx_outputs(self, unspent, tx_ins, tx_outs, tx):
        print ''
        print '** Transaction info **'
        print ''
        print 'Total unspent outputs before transaction: '
        print unspent
        print ''
        print 'Transaction inputs:'
        print tx_ins
        print ''
        print 'Transaction outputs:'
        print tx_outs
        print ''
        print 'Raw final transaction:'
        print tx
        print ''
        print 'Thank you for using Bitcoinista (Demo Mode)!'

    def draw_tx_start(self):
        print ''
        print 'Signing transaction...'

    def draw_mainnet_tx_finished(self):
        print ''
        print 'Transaction sent. Thank you for using Bitcoinista!'

        
