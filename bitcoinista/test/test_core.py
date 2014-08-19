import unittest
import bitcoinista

class TestCore(unittest.TestCase):

    def setUp(self):

        self.unspent = [{'output': '2818b4de824faa41539c4501cc68912e2da07a050b407024c56f8e622cc208c4:1', 'value': 10000000},
                        {'output': '58df9f2348323f46706d84e83b31d685e88100e21feab3a6bd91859670199c0a:1', 'value': 50000000},
                        {'output': '09604cfd3e2bfdef31e1404c93249023955634cd8686f02adaa7694ca6cafdea:3', 'value': 20000000}
                        ]

        self.balance = 80000000

    def test_balance(self):
        
        balance = bitcoinista.get_balance(self.unspent)
        self.assertEqual(balance, self.balance)

    def test_btc_satoshi_conversion(self):
        
        btc_val = 12.34567890
        sat_val = 1234567890
        self.assertEqual(sat_val, bitcoinista.btc_to_satoshi(btc_val))
        self.assertEqual(btc_val, bitcoinista.satoshi_to_btc(sat_val))

        btc_val = 0.0
        sat_val = 0
        self.assertEqual(sat_val, bitcoinista.btc_to_satoshi(btc_val))
        self.assertEqual(btc_val, bitcoinista.satoshi_to_btc(sat_val))

        btc_val = 0.00000001
        sat_val = 1
        self.assertEqual(sat_val, bitcoinista.btc_to_satoshi(btc_val))
        self.assertEqual(btc_val, bitcoinista.satoshi_to_btc(sat_val))

    def test_parse_bitcoin_uri(self):

        uri_amount = 0.25
        uri_address = '1AePfBmFQJVdvgxMV5MRs5trExecFq8rTR'
        uri_w_amount = 'bitcoin:{0}?amount={1}'.format(uri_address, uri_amount)
        uri_wo_amount = 'bitcoin:' + uri_address
        invalid_uri = 'buttcoin:' + uri_address

        addr, btc_amount = bitcoinista.parse_bitcoin_uri(uri_w_amount)
        self.assertEqual(addr, uri_address)
        self.assertEqual(btc_amount, uri_amount)

        addr, btc_amount = bitcoinista.parse_bitcoin_uri(uri_wo_amount)
        self.assertEqual(addr, uri_address)
        self.assertIsNone(btc_amount)
        
        addr, btc_amount = bitcoinista.parse_bitcoin_uri(invalid_uri)
        self.assertIsNone(addr)
        self.assertIsNone(btc_amount)

    def test_simple_tx_inputs_outputs(self):
        
        val_to_txhash = dict()
        for u in self.unspent:
            val_to_txhash[u['value']] = u['output']
            
        from_addr = '1AePfBmFQJVdvgxMV5MRs5trExecFq8rTR'
        to_addr = '1754QwNdYEhGWxNYu8ufAGEoqpVYPrxyZS'
        txfee = 10000

        from_addr_testnet = 'mkJp76EjHJhtAChdkNsX5PbiJFDWyzjWB4'
        to_addr_testnet_stealth = 'waPUuLLykSnY3itzf1AyrQZm42F7KyB7SR5zpfqmnzPXWhx9kXLzV3EcyqzDdpTwngiyCCMUqztS9S1d7XJs3JMt3MsHPDpBCudvx9'
        to_addr_stealth = 'vJmtjxSDxNPXL4RNapp9ARdqKz3uJyf1EDGjr1Fgqs9c8mYsVH82h8wvnA4i5rtJ57mr3kor1EVJrd4e5upACJd588xe52yXtzumxj'

        # Throw if not enough funds
        amount_to_send = 90000000
        self.assertRaises(Exception, bitcoinista.simple_tx_inputs_outputs, (from_addr, self.unspent, to_addr, amount_to_send, txfee))

        # The output with 10M satoshis should be completely consumed.
        # No change address.
        amount_to_send = 9990000
        inputs, outputs = bitcoinista.simple_tx_inputs_outputs(from_addr, self.unspent, to_addr, amount_to_send, txfee)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs[0]['value'], 10000000)
        self.assertEqual(inputs[0]['output'], val_to_txhash[10000000])
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0]['address'], to_addr)
        self.assertEqual(outputs[0]['value'], amount_to_send)

        # The output with 10M satoshis is used.
        # Change (5M satoshis) goes back to the sending address.
        amount_to_send = 4990000
        inputs, outputs = bitcoinista.simple_tx_inputs_outputs(from_addr, self.unspent, to_addr, amount_to_send, txfee)
        self.assertEqual(len(inputs), 1)
        self.assertEqual(inputs[0]['value'], 10000000)
        self.assertEqual(inputs[0]['output'], val_to_txhash[10000000])
        self.assertEqual(len(outputs), 2)

        to_sender = {'address' : to_addr, 'value' : amount_to_send}
        change = {'address' : from_addr, 'value' : 5000000}
        self.assertIn(to_sender, outputs)
        self.assertIn(change, outputs)

        # Outputs with 50M and 20M are used.
        # Change (5M) back to sending address
        amount_to_send = 64990000
        inputs, outputs = bitcoinista.simple_tx_inputs_outputs(from_addr, self.unspent, to_addr, amount_to_send, txfee)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs[0]['value'], 50000000)
        self.assertEqual(inputs[0]['output'], val_to_txhash[50000000])
        self.assertEqual(inputs[1]['value'], 20000000)
        self.assertEqual(inputs[1]['output'], val_to_txhash[20000000])
        self.assertEqual(len(outputs), 2)

        to_sender = {'address' : to_addr, 'value' : amount_to_send}
        change = {'address' : from_addr, 'value' : 5000000}
        self.assertIn(to_sender, outputs)
        self.assertIn(change, outputs)

        # Send to stealth address
        # Outputs with 50M and 20M are used.
        # Change (5M) back to sending address
        amount_to_send = 64990000
        inputs, outputs = bitcoinista.simple_tx_inputs_outputs(from_addr_testnet, self.unspent, to_addr_testnet_stealth, amount_to_send, txfee)
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs[0]['value'], 50000000)
        self.assertEqual(inputs[0]['output'], val_to_txhash[50000000])
        self.assertEqual(inputs[1]['value'], 20000000)
        self.assertEqual(inputs[1]['output'], val_to_txhash[20000000])
        self.assertEqual(len(outputs), 3)

        self.assertIn('script', outputs[0])
        self.assertEqual(amount_to_send, outputs[1]['value'])
        change = {'address' : from_addr_testnet, 'value' : 5000000}
        self.assertEqual(change, outputs[2])

        # Stealth address disabled on mainnet
        # Should throw if sending from mainnet to testnet
        self.assertRaises(Exception, bitcoinista.simple_tx_inputs_outputs, from_addr, self.unspent, to_addr_stealth, amount_to_send, txfee)
        self.assertRaises(Exception, bitcoinista.simple_tx_inputs_outputs, from_addr, self.unspent, from_addr_testnet, amount_to_send, txfee)
        
        # Empty out wallet. All outputs are used.
        # No change back.
        amount_to_send = 79990000
        inputs, outputs = bitcoinista.simple_tx_inputs_outputs(from_addr, self.unspent, to_addr, amount_to_send, txfee)
        self.assertEqual(sorted(self.unspent), sorted(inputs))
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0]['address'], to_addr)
        self.assertEqual(outputs[0]['value'], amount_to_send)

    def test_is_address_valid(self):

        good_mainnet_addr = '1AePfBmFQJVdvgxMV5MRs5trExecFq8rTR'
        bad_mainnet_addr  = '1AePfBmFQJWdvgxMV5MRs5trExecFq8rTR'
        good_mainnet_p2sh = '31oSGBBNrpCiENH3XMZpiP6GTC4tad4bMy'
        bad_mainnet_p2sh  = '31oSGBBNrpCiENH4XMZpiP6GTC4tad4bMy'
        good_testnet_addr = 'msj42CCGruhRsFrGATiUuh25dtxYtnpbTx'
        bad_testnet_addr  = 'msj42CCGruhRsFrGATiUuh25dtxYTnpbTx'
        good_testnet_p2sh = '2MzQwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc'
        bad_testnet_p2sh  = '2MzqwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc'
        good_mainnet_stealth = 'vJmtjxSDxNPXL4RNapp9ARdqKz3uJyf1EDGjr1Fgqs9c8mYsVH82h8wvnA4i5rtJ57mr3kor1EVJrd4e5upACJd588xe52yXtzumxj'
        bad_mainnet_stealth  = 'vJmtjxSDxNPXL4RNapp9BRdqKz3uJyf1EDGjr1Fgqs9c8mYsVH82h8wvnA4i5rtJ57mr3kor1EVJrd4e5upACJd588xe52yXtzumxj'
        good_testnet_stealth = 'waPUuLLykSnY3itzf1AyrQZm42F7KyB7SR5zpfqmnzPXWhx9kXLzV3EcyqzDdpTwngiyCCMUqztS9S1d7XJs3JMt3MsHPDpBCudvx9'
        bad_testnet_stealth  = 'waPUuLLykSnY3itzf1AyrQZm42F7KyB7SR5zpAqmnzPXWhx9kXLzV3EcyqzDdpTwngiyCCMUqztS9S1d7XJs3JMt3MsHPDpBCudvx9'
        
        # Mainnet
        self.assertTrue(bitcoinista.is_address_valid(good_mainnet_addr))
        self.assertFalse(bitcoinista.is_address_valid(bad_mainnet_addr, on_testnet=False))
        self.assertTrue(bitcoinista.is_address_valid(good_mainnet_p2sh))
        self.assertFalse(bitcoinista.is_address_valid(bad_mainnet_p2sh, on_testnet=False))
        self.assertTrue(bitcoinista.is_address_valid(good_mainnet_stealth))
        self.assertFalse(bitcoinista.is_address_valid(bad_mainnet_stealth, on_testnet=False))

        # Testnet
        self.assertTrue(bitcoinista.is_address_valid(good_testnet_addr, on_testnet=True))
        self.assertFalse(bitcoinista.is_address_valid(bad_testnet_addr, on_testnet=True))
        self.assertTrue(bitcoinista.is_address_valid(good_testnet_p2sh, on_testnet=True))
        self.assertFalse(bitcoinista.is_address_valid(bad_testnet_p2sh, on_testnet=True))
        self.assertTrue(bitcoinista.is_address_valid(good_testnet_stealth, on_testnet=True))
        self.assertFalse(bitcoinista.is_address_valid(bad_testnet_stealth, on_testnet=True))
                
if __name__ == '__main__':
    unittest.main()
