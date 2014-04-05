#Bitcoinista: Simple python bitcoin wallet for iOS#

Bitcoinista is a simple text-based bitcoin wallet for spending small
amounts of bitcoin on the go. It can run on the desktop but the main
usecase is to run it in the sandboxed python app
[Pythonista](http://omz-software.com/pythonista/) on iOS. Within this
environment Bitcoinista is able to sign transactions and relay them to
the bitcoin network, allowing you to spend your coins on your iPhone
or iPad without your private key ever leaving your device.

Bitcoinista is built on the excellent
[pybitcointools](https://github.com/vbuterin/pybitcointools) library
which is leightweight enough to be run in Pythonista. It also uses
[SlowAES](https://code.google.com/p/slowaes/) which is a pure python
implementation of AES.

##Installation##

To install Bitcoinista on your iOS device, go to installer.py in the
bitcoinista repository, the raw code is here:
[installer.py](https://raw.githubusercontent.com/christianlundkvist/bitcoinista/master/installer.py).

Select all the code and copy it. Go to Pythonista, create a new script
in the Script Library and paste the code in there. Now run it. This
will install bitcoinista, pybitcointools and slowaes.

The main script to run is ```bitcoinista.py``` in the main script
library.

##Usage##

###Creating wallet###

The first time you start Bitcoinista, you will be asked to create a
wallet. The wallet is just a single address/private key pair, and you
can create it by:

* Importing your own private key in WIF format

* Letting Bitcoinista create a random key using
  ```pybitcointools.random_key()```.

* Supplying a brainwallet passphrase if you like using diceware or
  similar system to control your own randomness. We strongly advice
  against using less than 128 bits of entropy for this passphrase.

###Transaction from bitcoin URI###

When scanning a QR code from a merchant the contents of the code looks something like

'''
bitcoin:1BMjTvpSzsRYFEutYjx3AnTC49z4Pk8r7i?amount=0.01&label=starbucks
'''

You can scan such a QR code and copy the corresponding URI. When
Bitcoinista notices a bitcoin URI in the clipboard a transaction is
automatically created with the above address and amount. All you need
to do is to enter your password and the transaction is sent.

###Manual transaction###

If no bitcoin URI is in the clipboard Bitcoinista will ask you to
enter the address and the amount you wish to send.

##Features##

* Runs on iOS, no jailbreak needed.

* Unjailbroken iOS security features: App environment is sandboxed, all
  software signed by Apple, hardware encryption.

* Quickly spend from a scanned QR code.

* Private key encrypted with AES if your phone is stolen. Remember to
  back up your key!

* Can input your own private key


##Limitations##

* Depends on paid software (Pythonista is $6.99 in the App Store)

* Single address in wallet: No change addresses or BIP32 support (at this time)

* Only simple transactions: can only send to a single address
