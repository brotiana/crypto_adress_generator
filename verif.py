from bip_utils import Bip39MnemonicValidator
import os
MNEMONIC = os.getenv("TRON_MNEMONIC")
Bip39MnemonicValidator().Validate(MNEMONIC)
print("Seed BIP39 valide")
