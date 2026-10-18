import streamlit as st

from hamming_simulator import (
    encode_hamming,
    display_codeword,
    transmit,
    receive,
)

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Hamming Code Simulator",
    page_icon="📡",
    layout="wide",
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

.main-heading {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
}

.sub-heading {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}

.bit-box {
    padding: 14px 8px;
    border: 1px solid #94a3b8;
    border-radius: 10px;
    text-align: center;
    font-family: monospace;
    font-size: 23px;
    font-weight: bold;
    letter-spacing: 3px;
    overflow-wrap: anywhere;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-heading">📡 Hamming Code Simulator</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-heading">'
    'Interactive Data Transmission & Error Correction Lab'
    '</div>',
    unsafe_allow_html=True,
)

st.info(
    "Explore how parity bits detect and correct single-bit "
    "errors during data transmission."
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Simulation Settings")
st.sidebar.write("Configure your transmission experiment.")

data = st.sidebar.text_input(
    "Enter binary data",
    value="1011",
).strip()

mode = st.sidebar.radio(
    "Transmission mode",
    [
        "Normal Transmission",
        "Inject Single-Bit Error",
    ],
)

position = None
input_error = None

# Calculate valid codeword length before displaying position selector
if data and all(bit in "01" for bit in data):
    try:
        codeword_length = len(encode_hamming(data)) - 1

        if mode == "Inject Single-Bit Error":
            position = st.sidebar.number_input(
                "Bit position (counting from right)",
                min_value=1,
                max_value=codeword_length,
                value=min(6, codeword_length),
                step=1,
            )

    except (ValueError, TypeError) as error:
        input_error = str(error)

run = st.sidebar.button(
    "🚀 Run Simulation",
    type="primary",
    use_container_width=True,
)

# ---------------- INITIAL SCREEN ----------------
if not run:
    st.subheader("Communication Workflow")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📤 Transmitter")
        st.write("Enter binary data and generate Hamming code.")

    with col2:
        st.markdown("### 📡 Communication Channel")
        st.write("Transmit data with or without a bit error.")

    with col3:
        st.markdown("### 📥 Receiver")
        st.write("Calculate the syndrome and recover data.")

    st.divider()
    st.subheader("Project Features")

    left, right = st.columns(2)

    with left:
        st.success("✓ Hamming code encoding")
        st.success("✓ Single-bit error injection")
        st.success("✓ Syndrome calculation")

    with right:
        st.success("✓ Error correction")
        st.success("✓ Original data recovery")
        st.success("✓ Visual results dashboard")

# ---------------- RUN SIMULATION ----------------
if run:
    try:
        if not data or any(bit not in "01" for bit in data):
            raise ValueError(
                "Please enter a non-empty binary string containing only 0 and 1."
            )

        if input_error:
            raise ValueError(input_error)

        # 1. TRANSMITTER
        codeword = encode_hamming(data)
        original_codeword = display_codeword(codeword)

        # 2. COMMUNICATION CHANNEL
        error_positions = []

        if mode == "Inject Single-Bit Error":
            error_positions = [int(position)]

        # IMPORTANT:
        # This call matches the list-based transmit() function.
        received = transmit(codeword, error_positions)

        # 3. RECEIVER
        result = receive(received)

        st.divider()
        st.subheader("📊 Transmission Dashboard")

        m1, m2, m3 = st.columns(3)

        m1.metric("Original Data Bits", len(data))
        m2.metric("Codeword Length", len(codeword) - 1)
        m3.metric("Syndrome", result["syndrome"])

        st.divider()

        sender, channel, receiver = st.columns(3)

        # TRANSMITTER PANEL
        with sender:
            st.markdown("### 📤 Transmitter")
            st.caption("Original data")
            st.code(data)

            st.caption("Generated codeword")
            st.markdown(
                f'<div class="bit-box">{original_codeword}</div>',
                unsafe_allow_html=True,
            )

            st.caption("Parity bits are added before transmission.")

        # CHANNEL PANEL
        with channel:
            st.markdown("### 📡 Communication Channel")

            if error_positions:
                st.warning(
                    f"Bit position {error_positions[0]} was flipped."
                )
            else:
                st.success("No error introduced.")

            st.caption("Received codeword")
            st.markdown(
                f'<div class="bit-box">'
                f'{result["received_codeword"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # RECEIVER PANEL
        with receiver:
            st.markdown("### 📥 Receiver")
            st.caption("Syndrome value")

            st.metric("Syndrome", result["syndrome"])

            if result["error_detected"]:
                if result["error_position"] is not None:
                    st.warning(
                        "Error position: "
                        f'{result["error_position"]}'
                    )
                else:
                    st.warning("Non-zero syndrome detected.")
            else:
                st.success("No single-bit error detected.")

        # CORRECTION RESULTS
        st.divider()
        st.subheader("🛡️ Error Correction Results")

        result_left, result_right = st.columns(2)

        with result_left:
            st.markdown("**Corrected codeword**")
            st.code(result["corrected_codeword"])

        with result_right:
            st.markdown("**Recovered original data**")
            st.code(result["recovered_data"])

        if result["recovered_data"] == data:
            st.success(
                "Recovered data matches the original input."
            )
        else:
            st.warning(
                "Recovered data differs from the original input. "
                "Multiple-bit errors may not be corrected reliably."
            )

        # EXPLANATION
        with st.expander("Understand the result"):
            st.write(
                "The transmitter inserts parity bits into the data. "
                "The receiver recalculates the parity checks."
            )

            st.write(
                "The syndrome is the decimal value formed by the "
                "failed parity checks. Under the single-bit-error "
                "assumption, it identifies the incorrect bit position."
            )

            st.write(
                "A syndrome of zero means no error was detected by "
                "the parity checks; it does not guarantee that the "
                "received data is error-free."
            )

    except (ValueError, TypeError, IndexError) as error:
        st.error(f"Simulation error: {error}")

# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "T.Y. B.Tech CSE | Computer Networks Laboratory | "
    "Hamming Code-Based Data Communication Simulator"
) 