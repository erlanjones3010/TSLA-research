"""Peer P/E valuation using only Python's standard library.

Enter your target and peer inputs below. Prices are dollars per share and EPS
is diluted earnings per share. Leave an unavailable value as None.
"""

from statistics import median


# ============================== EDITABLE INPUTS ==============================
TARGET = {
    "ticker": "ABG",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {"ticker": "AN", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "price": 421.48, "diluted_eps": 36.81},
]
# ==============================================================================


def normalized_ticker(value):
    """Normalize tickers so case and surrounding whitespace do not duplicate."""
    return str(value).strip().upper()


def is_positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def price_text(value):
    return f"${value:.2f}" if value is not None else "not meaningful"


def multiple_text(value):
    return f"{value:.6f}x" if value is not None else "not meaningful"


def target_implied_price(peer_multiple, target_eps):
    if peer_multiple is None or not is_positive_number(target_eps):
        return None
    return peer_multiple * target_eps


def main():
    target_ticker = normalized_ticker(TARGET.get("ticker", ""))
    target_price = TARGET.get("price")
    target_eps = TARGET.get("diluted_eps")

    print(f"Target: {target_ticker or 'UNSPECIFIED'}")
    print(f"Target price: {price_text(target_price) if is_positive_number(target_price) else 'not meaningful'}")
    print(f"Target diluted EPS: {target_eps if is_positive_number(target_eps) else 'not meaningful'}")

    unique_peers = []
    seen = set()
    for peer in PEERS:
        ticker = normalized_ticker(peer.get("ticker", ""))
        if not ticker:
            print("Excluded peer with missing ticker.")
            continue
        if ticker == target_ticker:
            print(f"Excluded {ticker}: it is the target.")
            continue
        if ticker in seen:
            print(f"Excluded duplicate peer: {ticker}.")
            continue
        seen.add(ticker)
        unique_peers.append(
            {
                "ticker": ticker,
                "price": peer.get("price"),
                "diluted_eps": peer.get("diluted_eps"),
            }
        )

    valid_multiples = []
    print("\nPeer P/E multiples:")
    for peer in unique_peers:
        price = peer["price"]
        eps = peer["diluted_eps"]
        if not is_positive_number(price) or not is_positive_number(eps):
            peer["pe"] = None
            print(f"  {peer['ticker']}: not meaningful (price and diluted EPS must both be positive)")
        else:
            peer["pe"] = price / eps
            valid_multiples.append(peer["pe"])
            print(f"  {peer['ticker']}: {multiple_text(peer['pe'])}")

    print("\nPeer valuation:")
    if not valid_multiples:
        full_estimate = None
        print("  No usable peers; no estimate.")
    elif len(valid_multiples) == 1:
        reference_multiple = valid_multiples[0]
        full_estimate = target_implied_price(reference_multiple, target_eps)
        print(f"  One valid peer; reference P/E: {multiple_text(reference_multiple)}")
        print(f"  Reference implied price: {price_text(full_estimate)}")
    else:
        minimum_multiple = min(valid_multiples)
        median_multiple = median(valid_multiples)
        maximum_multiple = max(valid_multiples)
        full_estimate = target_implied_price(median_multiple, target_eps)
        print(f"  Minimum P/E: {multiple_text(minimum_multiple)} | Implied price: {price_text(target_implied_price(minimum_multiple, target_eps))}")
        print(f"  Median P/E:  {multiple_text(median_multiple)} | Implied price: {price_text(full_estimate)}")
        print(f"  Maximum P/E: {multiple_text(maximum_multiple)} | Implied price: {price_text(target_implied_price(maximum_multiple, target_eps))}")

    print("\nPeer-removal sensitivity (median-implied price):")
    if not unique_peers:
        print("  No peers to remove.")
        return
    for removed_peer in unique_peers:
        remaining = [peer["pe"] for peer in unique_peers if peer is not removed_peer and peer["pe"] is not None]
        if not remaining:
            print(f"  Remove {removed_peer['ticker']}: no estimate.")
            continue
        remaining_price = target_implied_price(median(remaining), target_eps)
        if remaining_price is None or full_estimate is None:
            change = "not meaningful"
        else:
            # Both figures are unrounded floats; only display is rounded.
            change = f"${remaining_price - full_estimate:.2f}"
        print(
            f"  Remove {removed_peer['ticker']}: {price_text(remaining_price)} "
            f"(change from full-peer estimate: {change})"
        )


if __name__ == "__main__":
    main()
