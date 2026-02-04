import os
from bip_utils import Bip39SeedGenerator

MNEMONIC = os.getenv("TRON_MNEMONIC")

if not MNEMONIC:
    raise Exception("TRON_MNEMONIC non définie")

seed_bytes = Bip39SeedGenerator(MNEMONIC).Generate()
print("Seed chargée correctement")
