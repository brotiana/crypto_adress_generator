#generer les adresse ltc
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

# =========================
# CONFIGURATION
# =========================

MNEMONIC = "describe laptop cinnamon habit birth scale rely humble swarm furnace dignity economy"
START_INDEX = 0
COUNT = 5

# =========================
# GENERATION
# =========================

def generate_ltc_addresses(mnemonic, start, count):
    print("Chargement de la seed...")
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    print("Seed OK\n")

    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.LITECOIN)

    wallets = []

    for i in range(start, start + count):
        acc = (
            bip44_mst
            .Purpose()
            .Coin()
            .Account(0)
            .Change(Bip44Changes.CHAIN_EXT)
            .AddressIndex(i)
        )

        wallets.append({
            "index": i,
            "address": acc.PublicKey().ToAddress(),
            "private_key_wif": acc.PrivateKey().ToWif()
        })

    return wallets

# =========================
# MAIN
# =========================

def main():
    wallets = generate_ltc_addresses(MNEMONIC, START_INDEX, COUNT)

    print("Adresses Litecoin générées :\n")

    for w in wallets:
        print(f"Index        : {w['index']}")
        print(f"Adresse LTC  : {w['address']}")
        print(f"Clé privée   : {w['private_key_wif']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
