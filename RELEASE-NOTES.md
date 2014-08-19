# Release Notes #

## Version 0.3.1 - 2014-08-18 ##

* Add USD exchange rate.

* Fixed erroneous magic byte for testnet P2SH addresses.

* Updated tests.

## Version 0.3 - 2014-07-23 ##

* Add support for sending to *basic stealth addresses*, i.e. stealth
addresses that have one scan key, one spend key, and no prefix.

* Fixed inconsistent handling of imported compressed keys.

* Demo mode now uses testnet addresses.

* Removed the ability to use a brainwallet passphrase to create the
  private key.

## Version 0.2 - 2014-06-10 ##

* Added full support for testnet using the testnet APIs from
  [blockr.io][blockr] recently introduced in [pybitcointools][].

* Now fully supports sending to P2SH addresses.

## Version 0.1.1 - 2014-06-01 ##

Removed `main.py` and refactored the code therein using a
Model-View-Controller paradigm. New files are `model.py`,
`text_view.py`, `text_controller.py`.

The cause of the recursion limit bug was that Pythonista resets the
recursion limit in the interpreter to 256 which caused some functions
in `pybitcointools` to exceed the recursion limit. This was fixed by
manually resetting the recursion limit to 1000 in `bitcoinista.py`.

## Version 0.1 - 2014-04-18 ##

Initial release. Included features:

* Create wallet from either random key, brainwallet passphrase or imported key
  in WIF format.
* Send bitcoins either manually or from URI in clipboard.
* AES encryption of private key.

[pybitcointools]: https://github.com/vbuterin/pybitcointools
[blockr]: http://blockr.io
