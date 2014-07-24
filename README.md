# Bitcoinista: Simple python bitcoin wallet for iOS #

Bitcoinista is a simple bitcoin wallet with a text-based UI for spending small
amounts of bitcoin on the go. It can run on the desktop but the main usecase is
to run it in the sandboxed python app [Pythonista][] on iOS. Within this
environment Bitcoinista is able to sign transactions and relay them to the
bitcoin network, allowing you to spend your coins on your iPhone or iPad without
your private key ever leaving your device.

Bitcoinista is built on the excellent [pybitcointools][] library which is
lightweight enough to be run in Pythonista. It also uses [SlowAES][] which is a
pure python implementation of AES.

## Installation ##

To install Bitcoinista on your iOS device, first go to [installer.py][inst] in
the Bitcoinista repository.

Select all the code and copy it. Go to Pythonista, create a new script in the
Script Library and paste the code in there. Now run it. This will install two
folders `bitcoinista`, `pybitcointools` and two files `bitcoinista.py` and
`aes.py`, where `bitcoinista.py` is the main script to run.

A video describing the installation can be found here:

<http://youtu.be/Q2e3sX3Lkn0>

If you want a shortcut to Bitcoinista on your home screen you can go
[here][omzicon], write "bitcoinista" (note the lower case) as script name, and
then add the page to your homescreen.

## Usage ##

### Creating wallet ###

The first time you start Bitcoinista, you will be asked to create a wallet. The
wallet is just a single address/private key pair, and you can create it in one
of three ways:

* Importing your own private key in WIF format.

* Letting Bitcoinista create a random key using `pybitcointools.random_key()`

* Supplying a brainwallet passphrase if you like using [diceware][] or
  similar system to control your own randomness. **We strongly advice
  against using less than 128 bits of entropy for this passphrase.**

Once you've created the wallet you will be asked to select a password
for the AES encryption of the private key. Once you've done this the
wallet file `bitcoinista_wallet.json` will be created, containing the
address and encrypted private key.

### Transaction from bitcoin URI ###

When scanning a QR code from a merchant the contents of the code is
often a [Bitcoin URI][btcuri] and looks something like

    bitcoin:1BMjTvpSzsRYFEutYjx3AnTC49z4Pk8r7i?amount=0.01&label=starbucks

You can scan such a QR code and copy the corresponding URI. When
Bitcoinista notices a bitcoin URI in the clipboard a transaction is
automatically created with the above address and amount. All you need
to do is to enter your password and transaction fee and the
transaction is sent.

A video demonstrating sending from a bitcoin URI is here:

<http://youtu.be/JBRK0YJYMck>

### Manual transaction ###

If no bitcoin URI is in the clipboard Bitcoinista will ask you to
enter the address to send to and the amount you wish to send.

## Features ##

* Runs on iOS, no jailbreak needed.

* Open source: Runs directly from the python source for complete
  transparency.

* Quickly spend using a scanned QR code.

* Private key encrypted with AES in case your phone is lost or
  stolen. Remember to back up your key!

* Ability to import your own private key to spend from paper wallet
  etc.

* Testnet support for playing around without risking real bitcoins.

* Ability to send to stealth addresses. See below.

## Limitations ##

* Needs paid software to run on iOS: Pythonista is $6.99 in the App
  Store. Note that this author is not affiliated with Pythonista in
  any way.

* Single address in wallet: No change addresses or BIP32 support.

* Only simple transactions: Unable to send to more than one address at
  a time.

* No GUI: Simple, text-based interface.

## Stealth Address support ##

Bitcoinista supports sending to [stealth addresses][stealth]. This is
an experimental feature and is only supported in Testnet and Demo
modes at this time.

Stealth addresses are special addresses that can be reused for
receiving payments without impacting privacy. When sending to a
stealth address a random temporary bitcoin address is created where
the payment is sent. At the same time an *ephemeral public key* is
created and stored in the blockchain. The owner of the stealth address
can use the ephemeral public key together with his stealth private
keys to create the private key to the temporary address and redeem the
payment.

An example of wallet software that uses stealth addresses is the
feature-rich [Dark Wallet][] (currently in Alpha).

## Testnet mode ##

If you set the flag `user_mode='testnet'` in the script
`bitcoinista.py` you'll be able to run Bitcoinista in testnet
mode. Bitcoinista will generate a testnet address and can send and
receive testnet coins as you would bitcoins. All you need to do is to
grab a few coins from a [testnet faucet][testfaucet] and you can start
testing.

## Demo mode ##

If you set the flag `user_mode='demo'` in the script `bitcoinista.py`
you can run Bitcoinista in demo mode. In this mode you will always
have 0.8 fake coins in your wallet and you can run Bitcoinista as you
normally would. Instead of sending a transaction to the network
Bitcoinista will simply display the inputs and outputs of the
transactions so you can see which unspent outputs are selected, if the
correct amount of change is sent etc. This is a good way of playing
around with the interface without risking any coins. Demo mode also
works with no internet connection.

## Troubleshooting ##

If you install a newer version or remove Bitcoinista and install again
you will have to restart Pythonista for the changes to take effect.
You can do this by double clicking the home button and swipe up on the
Pythonista app.


[btcuri]: https://github.com/bitcoin/bips/blob/master/bip-0021.mediawiki
[omzicon]: http://omz-software.com/pythonista/shortcut/
[pybitcointools]: https://github.com/vbuterin/pybitcointools
[pythonista]: http://www.omz-software.de/pythonista/
[slowaes]: https://code.google.com/p/slowaes/
[diceware]: http://world.std.com/~reinhold/diceware.html
[inst]: https://github.com/christianlundkvist/bitcoinista/blob/master/installer.py
[testfaucet]: http://tpfaucet.appspot.com
[stealth]: http://sourceforge.net/p/bitcoin/mailman/message/31813471/
[dark wallet]: https://github.com/darkwallet/darkwallet
