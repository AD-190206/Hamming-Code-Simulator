"""Hamming Code Simulator - Backend Logic
Uses even parity and corrects single-bit errors.
Bit positions are counted from the right, starting at 1.
"""

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


def validate_binary(data):
    data = str(data).strip()
    if not data or any(bit not in "01" for bit in data):
        raise ValueError("Enter binary data containing only 0 and 1.")
    return data


def encode_hamming(data):
    data = validate_binary(data)
    m = len(data)
    r = 0

    while 2 ** r < m + r + 1:
        r += 1

    n = m + r
    bits = [0] * (n + 1)

    j = 0
    for pos in range(1, n + 1):
        if not is_power_of_two(pos):
            bits[pos] = int(data[j])
            j += 1

    # Calculate even parity bits
    for p in (2 ** i for i in range(r)):
        parity = 0
        for pos in range(1, n + 1):
            if pos & p:
                parity ^= bits[pos]
        bits[p] = parity

    return bits


def display_codeword(bits):
    return "".join(str(bits[pos]) for pos in range(len(bits) - 1, 0, -1))


def transmit(codeword, error_positions=None):
    """Flip the requested bit positions."""
    received = codeword.copy()
    error_positions = [] if error_positions is None else error_positions

    if not isinstance(error_positions, list):
        raise TypeError("error_positions must be a list, e.g. [6].")

    n = len(received) - 1

    for pos in error_positions:
        if not isinstance(pos, int) or isinstance(pos, bool):
            raise ValueError("Bit positions must be integers.")
        if not 1 <= pos <= n:
            raise ValueError(f"Bit position must be between 1 and {n}.")
        received[pos] ^= 1

    return received


def receive(bits):
    """Calculate syndrome and attempt single-bit correction."""
    corrected = bits.copy()
    n = len(corrected) - 1
    syndrome = 0
    p = 1

    while p <= n:
        parity = 0

        for pos in range(1, n + 1):
            if pos & p:
                parity ^= corrected[pos]

        if parity != 0:
            syndrome += p

        p *= 2

    error_detected = syndrome != 0
    correction_attempted = False
    error_position = None

    if error_detected and syndrome <= n:
        error_position = syndrome
        corrected[syndrome] ^= 1
        correction_attempted = True

    recovered_data = "".join(
        str(corrected[pos])
        for pos in range(1, n + 1)
        if not is_power_of_two(pos)
    )

    return {
        "received_codeword": display_codeword(bits),
        "syndrome": syndrome,
        "error_detected": error_detected,
        "error_position": error_position,
        "corrected_codeword": display_codeword(corrected),
        "recovered_data": recovered_data,
        "correction_attempted": correction_attempted,
    }
