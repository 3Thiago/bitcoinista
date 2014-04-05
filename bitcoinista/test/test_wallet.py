import unittest, os
import bitcoinista
import pybitcointools as bc

class TestWallet(unittest.TestCase):

    def setUp(self):
        self.brainwallet_string = 'Here is a brainwallet string for testing purposes'
        self.private_key = bc.sha256(self.brainwallet_string)
        self.private_key_wif = bc.encode_privkey(self.private_key, 'wif')
        self.addr = bc.privkey_to_address(self.private_key)
        
        #print self.brainwallet_string
        #print self.private_key
        #print self.private_key_wif

    def test_encrypt_decrypt(self):
        
        # Roundtrip clear -> enc -> clear
        pw = 'testpassword'
        encr_privkey = bitcoinista.encrypt_privkey(self.private_key, pw)
        decrypted_privkey = bitcoinista.decrypt_privkey(encr_privkey, pw)

        self.assertNotEqual(encr_privkey, self.private_key)
        self.assertEqual(decrypted_privkey, self.private_key)

        # Roundtrip enc -> clear -> enc is not equal since
        # this implementation of AES is non-deterministic

    def test_privkey_from_input(self):

        prv_bw, method = bitcoinista.privkey_from_user_input(self.brainwallet_string)
        self.assertEqual(prv_bw, self.private_key)
        self.assertEqual(method, 'brain')

        prv_from_wif, method = bitcoinista.privkey_from_user_input(self.private_key_wif)
        self.assertEqual(prv_from_wif, self.private_key)
        self.assertEqual(method, 'wif')

        prv_random, method = bitcoinista.privkey_from_user_input('')
        prv_random2, method2 = bitcoinista.privkey_from_user_input('')
        
        self.assertEqual(bc.get_privkey_format(prv_random), 'hex')
        self.assertNotEqual(prv_random, prv_random2)
        self.assertEqual(method, 'random')
        self.assertEqual(method2, 'random')

    def test_wallet_file(self):
        
        filename = 'testing_wallet.json'

        pw = 'testpassword'
        encr_privkey = bitcoinista.encrypt_privkey(self.private_key, pw)
        
        bitcoinista.create_wallet_file(filename, encr_privkey, self.addr)
        encr_privkey2, addr2 = bitcoinista.read_from_wallet_file(filename)

        self.assertEqual(encr_privkey, encr_privkey2)
        self.assertEqual(self.addr, addr2)
        
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
