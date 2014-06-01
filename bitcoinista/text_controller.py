
from model import Model, PasswordError
from text_view import TextView
    
class TextController:
    
    def __init__(self, user_mode = 'mainnet'):
        self.user_mode = user_mode
        self.model = Model(user_mode)
        self.view = TextView()
        
    def run(self):
        
        self.view.draw_splash_screen(self.user_mode)
        
        found_wallet = True
        try:
            self.model.load_wallet()
        except OSError:
            found_wallet = False
            
        if not found_wallet:
            method = self.view.request_create_wallet_method()
            input = None
            if method != 'random':
                input = self.view.request_create_wallet_input(method)
            pw = None
            while pw is None:
                pw = self.view.request_wallet_pw(ask_twice=True)
            
            self.model.create_wallet(method, input, pw)
            self.model.load_wallet()
            wif_privkey = self.model.get_wif_privkey(pw)
            addr = self.model.get_address()
            self.view.draw_create_wallet_result(method, input, wif_privkey, addr)
            return
        
        addr = self.model.get_address()
        balance = self.model.get_balance()
        self.view.draw_address_and_balance(addr, balance)
        if balance == 0.0:
            self.view.draw_zero_balance()
            return

        self.view.draw_new_transaction()

        clipboard_exists = False
        try:
            import clipboard
            clipboard_exists = True
        except:
            pass
            
        destination_addr = None
        btc_send_amount = None

        if clipboard_exists:
            clipboard_input = clipboard.get()
            destination_addr, btc_send_amount = self.model.parse_bitcoin_uri(clipboard_input)

        if destination_addr is None:
            destination_addr = self.view.request_destination_address()
            if destination_addr == '':
                self.view.draw_abort()
                return
            else:
                self.model.set_destination_addr(destination_addr)
        else:
            self.model.set_destination_addr(destination_addr)
            self.view.draw_destination_address(destination_addr)
            
        if btc_send_amount is None:
            btc_send_amount = self.view.request_send_amount()
            if btc_send_amount == '':
                self.view.draw_abort()
                return
            else:
                btc_send_amount = float(btc_send_amount)
        else:
            self.view.draw_send_amount(btc_send_amount)
        self.model.set_send_amount(btc_send_amount)
        
        default_btc_txfee = self.model.get_txfee()
        btc_txfee = self.view.request_txfee(default_btc_txfee)
        msg = self.model.set_txfee(btc_txfee)
        if msg == 'OK':
            pass
        elif msg == 'ZERO' or msg == 'LARGE':
            selection = self.view.draw_txfee_warning(msg, btc_txfee)
            if selection != 'y':
                self.view.draw_abort()
                return

        if not self.model.is_balance_sufficient():
            self.view.draw_insufficient_balance()
            self.view.draw_abort()
            return
                            
        wrong_pw = True
        while wrong_pw:
            pw = self.view.request_wallet_pw(ask_twice=False)
            if pw == '' or pw == '\n':
                self.view.draw_abort()
                return
            try:
                tx_ins, tx_outs, tx = self.model.sign_tx(pw)
                wrong_pw = False
            except PasswordError:
                continue
        
        if self.user_mode == 'demo':
            self.view.draw_tx_start()
            unspent = self.model.get_unspent()
            self.view.draw_demo_tx_outputs(unspent, tx_ins, tx_outs, tx)
        elif self.user_mode == 'mainnet':
            self.view.draw_tx_start()
            self.model.push_tx(tx)
            self.view.draw_mainnet_tx_finished()
        else:
            raise Exception('Unsupported user mode ' + self.user_mode)
            
        return
