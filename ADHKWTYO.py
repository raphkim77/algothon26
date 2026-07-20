import numpy as np

nInst = 51
currentPos = np.zeros(nInst, dtype=int)

momentum_instruments = np.array([
    1, 3, 4, 7, 9, 13, 19, 20, 23, 28, 38, 45, 46, 49, 50
])

mean_reversion_instruments = np.array([
    0, 2, 5, 6, 8, 10, 11, 12, 14, 15, 16, 17, 18, 21, 22, 24, 25,
    26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44,
    47, 48
])


def getMyPosition(prcSoFar):
    global currentPos

    nins, nt = prcSoFar.shape

    lookback = 80
    if nt <= lookback:
        currentPos = np.zeros(nins, dtype=int)
        return currentPos

    current_prices = prcSoFar[:, -1]
    past_prices = prcSoFar[:, -1 - lookback]

    returns = np.log(current_prices / past_prices)

    signal = np.zeros(nins)

    # Mean reversion group:
    # if it went up, short it; if it went down, buy it
    signal[mean_reversion_instruments] = -returns[mean_reversion_instruments]

    # Momentum group:
    # if it went up, buy it; if it went down, short it
    signal[momentum_instruments] = returns[momentum_instruments]

    # Make signal market-neutral
    signal = signal - np.mean(signal)

    # Clean weird values
    signal = np.nan_to_num(signal, nan=0.0, posinf=0.0, neginf=0.0)

    total_signal = np.sum(np.abs(signal))
    if total_signal < 1e-12:
        return currentPos

    gross_exposure = 600000.0

    dollar_positions = gross_exposure * signal / total_signal
    target_pos = dollar_positions / current_prices

    currentPos = target_pos.astype(int)

    return currentPos