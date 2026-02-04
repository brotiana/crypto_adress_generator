# 1- on genere avec cette code le seed phrase de 12 mots
# apres , on : export TRON_MNEMONIC="mot1 mot2 mot3 ... mot12" 
# apres , on lance litecoin_adresse.py pour generer les adresses litecoin
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum

mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
print(mnemonic)
