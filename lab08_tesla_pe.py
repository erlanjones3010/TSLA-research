"""Lab 08 Tesla peer-P/E reference valuation (USD, GAAP diluted EPS)."""

from statistics import median


VALUATION_DATE = "2026-09-01"
TARGET = {"ticker": "TSLA", "price": 356.09, "diluted_eps": 1.08}

# Include only candidates classified as use or qualify in lab08_analysis.md.
PEERS = [
    {"ticker": "GM", "classification": "qualify", "price": 85.63, "diluted_eps": 3.27},
]


def positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def main():
    target_eps = TARGET["diluted_eps"]
    if not positive_number(target_eps):
        raise SystemExit("Target diluted EPS must be positive for P/E valuation.")

    print(f"Valuation date: {VALUATION_DATE}")
    print(f"Target: {TARGET['ticker']} | price ${TARGET['price']:.2f} | diluted EPS ${target_eps:.2f}")
    print(f"Target P/E: {TARGET['price'] / target_eps:.6f}x")

    multiples = []
    for peer in PEERS:
        if peer["classification"] not in {"use", "qualify"}:
            continue
        if not positive_number(peer["price"]) or not positive_number(peer["diluted_eps"]):
            print(f"{peer['ticker']}: not meaningful")
            continue
        multiple = peer["price"] / peer["diluted_eps"]
        multiples.append(multiple)
        print(f"{peer['ticker']} ({peer['classification']}): {multiple:.6f}x")

    if not multiples:
        print("No admitted peer P/E multiples; no estimate.")
        return

    reference_multiple = median(multiples)
    implied_price = reference_multiple * target_eps
    label = "reference" if len(multiples) == 1 else "median"
    print(f"Peer {label} P/E: {reference_multiple:.6f}x")
    print(f"TSLA implied price: ${implied_price:.2f}")

    print("Peer-removal sensitivity:")
    for peer in PEERS:
        remaining = [
            other["price"] / other["diluted_eps"]
            for other in PEERS
            if other is not peer
            and other["classification"] in {"use", "qualify"}
            and positive_number(other["price"])
            and positive_number(other["diluted_eps"])
        ]
        if not remaining:
            print(f"  Remove {peer['ticker']}: no peer-P/E estimate remains.")
        else:
            print(f"  Remove {peer['ticker']}: ${median(remaining) * target_eps:.2f}")


if __name__ == "__main__":
    main()
