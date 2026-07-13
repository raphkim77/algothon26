import numpy as np

nInst=51
currentPos = np.zeros(nInst)
def getMyPosition (prcSoFar):
    nins, nt = prcSoFar.shape

    # Need enough price history before trading
    lookback = 100
    if nt <= lookback:
        return np.zeros(nins)

    current_prices = prcSoFar[:, -1]

    # 100-day return
    past_prices = prcSoFar[:, -1 - lookback]
    returns = np.log(current_prices / past_prices)

    # Mean reversion signal:
    # If return was high, we short.
    # If return was low, we buy.
    signal = -returns

    # Market neutral:
    # removes general market direction so we are comparing instruments
    signal = signal - np.mean(signal)

    # Avoid divide-by-zero
    total_signal = np.sum(np.abs(signal))
    if total_signal < 1e-12:
        return np.zeros(nins)

    # Total dollar exposure.
    # Start moderate. Bigger is not always better because of risk and fees.
    gross_exposure = 200000

    dollar_positions = gross_exposure * signal / total_signal

    # Convert dollar position into number of shares
    positions = dollar_positions / current_prices

    return positions.astype(int)
