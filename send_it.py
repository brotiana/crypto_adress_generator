#on va envoyer quelque ltc sur un autre adresse
import requests
import math
from bitcoinlib.keys import Key
from ecdsa import SigningKey, SECP256k1, util
# =========================
# CONFIGURATION
# =========================

FROM_ADDRESS = "LSYqEJAtrx4uXywaP1cmTuuPWiK8FGb2ix"
FROM_PRIVATE_KEY_WIF = "T896jFc6VpvW6aLWULa65FodFKdVzgP1oKpCugEe6pFt4q1KGYAL"

TO_ADDRESS = "LZMdL5rqJ1chfM3St9sH4tzYnefMyCXYJy"

BLOCKCYPHER_API = "https://api.blockcypher.com/v1/ltc/main"
FEE_LITOSHI = 10_000  # ~0.0001 LTC

# =========================
# UTILS
# =========================
def litoshi_to_ltc(v):
    return v / 100_000_000

# =========================
# MAIN
# =========================
def main():
    print("Récupération des UTXO...")

    utxo_url = f"{BLOCKCYPHER_API}/addrs/{FROM_ADDRESS}?unspentOnly=true"
    utxo_data = requests.get(utxo_url, timeout=10).json()

    utxos = utxo_data.get("txrefs", [])
    if not utxos:
        raise Exception("Aucun UTXO disponible")

    total_litoshi = sum(u["value"] for u in utxos)
    total_ltc = litoshi_to_ltc(total_litoshi)
    print(f"Solde total : {total_ltc} LTC")

    send_litoshi = total_litoshi // 2 - FEE_LITOSHI
    if send_litoshi <= 0:
        raise Exception("Montant insuffisant après frais")

    print(f"Montant envoyé : {litoshi_to_ltc(send_litoshi)} LTC")
    print(f"Frais estimés  : {litoshi_to_ltc(FEE_LITOSHI)} LTC")

    # =========================
    # CREATE TX
    # =========================
    tx_skeleton = {
        "inputs": [{"addresses": [FROM_ADDRESS]}],
        "outputs": [{"addresses": [TO_ADDRESS], "value": send_litoshi}]
    }

    print("Création de la transaction...")
    tx = requests.post(f"{BLOCKCYPHER_API}/txs/new", json=tx_skeleton).json()
    if "errors" in tx:
        raise Exception(tx["errors"])

    # =========================
    # SIGN
    # =========================
    # --- clé correctement créée avant utilisation ---
    key = Key(import_key=FROM_PRIVATE_KEY_WIF, network="litecoin")
    pubkey_hex = key.public_hex

    # Use ECDSA to sign each 'tosign' digest with the private key, producing DER signatures hex-encoded
    sk = SigningKey.from_string(bytes.fromhex(key.private_hex), curve=SECP256k1)

    signatures = []
    for ts in tx["tosign"]:
        sig = sk.sign_digest(bytes.fromhex(ts), sigencode=util.sigencode_der)
        signatures.append(sig.hex())

    tx["signatures"] = signatures
    tx["pubkeys"] = [pubkey_hex]

    # =========================
    # SEND
    # =========================
    print("Diffusion de la transaction...")
    final_tx = requests.post(f"{BLOCKCYPHER_API}/txs/send", json=tx).json()
    if "errors" in final_tx:
        raise Exception(final_tx["errors"])

    print("Transaction envoyée avec succès")
    print("TX Hash :", final_tx["tx"]["hash"])


if __name__ == "__main__":
    main()
