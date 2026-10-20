import streamlit as st
import streamlit.components.v1 as components
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
codeword_length = None

# Calculate valid codeword length before displaying position selector.
# Use text_input so invalid edits (e.g. "abc", 0, or an out-of-range
# position) can be explicitly validated instead of silently retaining
# the number_input widget's previous valid value.
if data and all(bit in "01" for bit in data):
    try:
        codeword_length = len(encode_hamming(data)) - 1

        if mode == "Inject Single-Bit Error":
            position_input = st.sidebar.text_input(
                "Bit position (counting from right)",
                value=str(min(6, codeword_length)),
                key="error_position",
            ).strip()

            # Validate the text field and restore a subtle red invalid state
            # with an error icon, similar to Streamlit's native validation UI.
            position_error = None
            try:
                parsed_position = int(position_input)
                if not 1 <= parsed_position <= codeword_length:
                    position_error = (
                        f"Enter a position from 1 to {codeword_length}."
                    )
                else:
                    position = parsed_position
            except (ValueError, TypeError):
                position_error = "Enter a valid whole-number position."

            if position_error:
                st.sidebar.markdown(
                    """
                    <style>
                    /* Subtle invalid styling for the error-position field */
                    div[data-testid="stSidebar"] div[data-testid="stTextInput"]
                    input[aria-label="Bit position (counting from right)"] {
                        background-color: rgba(239, 68, 68, 0.08) !important;
                        border-color: #ef4444 !important;
                        box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.35) !important;
                    }
                    div[data-testid="stSidebar"] div[data-testid="stTextInput"]
                    input[aria-label="Bit position (counting from right)"]:focus {
                        background-color: rgba(239, 68, 68, 0.12) !important;
                        border-color: #dc2626 !important;
                        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2) !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                st.sidebar.error(f"⚠️ {position_error}")
            else:
                st.sidebar.caption(f"Selected position: {position}")

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

        # Show the role and value of each encoded bit.
        codeword_length = len(codeword) - 1

        # Validate the parsed position before any transmission occurs.
        if mode == "Inject Single-Bit Error":
            if position is None:
                st.error(
                    "Simulation cancelled: enter a valid bit position "
                    f"between 1 and {codeword_length}."
                )
                st.stop()

            if not 1 <= position <= codeword_length:
                st.error(
                    f"Invalid bit position. Choose a value from "
                    f"1 to {codeword_length}."
                )
                st.stop()

        bit_details = [
            {
                "Position (from right)": pos,
                "Bit value": codeword[pos],
                "Bit type": (
                    "Parity bit"
                    if pos & (pos - 1) == 0
                    else "Data bit"
                ),
            }
            for pos in range(1, codeword_length + 1)
        ]

        # 2. COMMUNICATION CHANNEL
        if mode == "Inject Single-Bit Error":
            error_positions = [position]
        else:
            error_positions = []

        # Transmit only after all input validation succeeds.
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

        with st.expander("Inspect transmission bit positions", expanded=True):
            st.caption(
                "Positions are numbered from the right, starting at 1. "
                "Parity bits occupy positions that are powers of 2."
            )

            bit_count = len(codeword) - 1

            # Convert the corrected display string back to the internal
            # position-indexed list used by the Hamming Code algorithm.
            corrected_bits = [0] + [
                int(bit) for bit in reversed(result["corrected_codeword"])
            ]

            def build_bit_cells(
                bits,
                highlight_errors=False,
                highlight_corrections=False,
            ):
                cells = []

                for pos in range(bit_count, 0, -1):
                    is_parity = (pos & (pos - 1)) == 0
                    css_class = "parity" if is_parity else "data"
                    label = "PARITY" if is_parity else "DATA"

                    bit_value = bits[pos]
                    cell_class = css_class

                    # Red: bit changed during transmission.
                    if (
                        highlight_errors
                        and bits[pos] != codeword[pos]
                    ):
                        cell_class = "error"

                    # Green: receiver changed the received bit.
                    elif (
                        highlight_corrections
                        and bits[pos] != received[pos]
                    ):
                        cell_class = "corrected"

                    cells.append(
                        f"""
                        <div class="cell-group">
                            <div class="bit-label {css_class}">
                                {label}
                            </div>
                            <div class="bit-cell {cell_class}">
                                {bit_value}
                            </div>
                            <div class="bit-position">
                                {pos}
                            </div>
                        </div>
                        """
                    )

                return "".join(cells)

            original_cells = build_bit_cells(codeword)

            received_cells = build_bit_cells(
                received,
                highlight_errors=True,
            )

            corrected_cells = build_bit_cells(
                corrected_bits,
                highlight_corrections=True,
            )

            html = f"""
            <style>
                * {{
                    box-sizing: border-box;
                }}

                .bit-row {{
                    display: grid;
                    grid-template-columns: repeat(
                        {bit_count}, minmax(0, 1fr)
                    );
                    gap: 6px;
                    font-family: sans-serif;
                    text-align: center;
                    width: 100%;
                }}

                .cell-group {{
                    min-width: 0;
                }}

                .bit-label {{
                    font-size: 10px;
                    font-weight: 700;
                    margin-bottom: 6px;
                    overflow-wrap: anywhere;
                    background: transparent;
                }}

                .bit-cell {{
                    background: #2b2b2b;
                    padding: 12px 2px;
                    border: 1px solid #444444;
                    border-radius: 8px;
                    font-size: 22px;
                    font-weight: 700;
                }}

                .data {{
                    color: #60a5fa;
                }}

                .parity {{
                    color: #fbbf24;
                }}

                .error {{
                    color: #fca5a5 !important;
                    background: #7f1d1d;
                    border: 1px solid #ef4444;
                }}

                .corrected {{
                    color: #86efac !important;
                    background: #14532d;
                    border: 1px solid #22c55e;
                }}

                .bit-position {{
                    margin-top: 6px;
                    font-size: 10px;
                    color: #a3a3a3;
                }}

                .section-title {{
                    margin: 16px 0 8px;
                    font: 600 12px sans-serif;
                    color: #b3b3b3;
                }}

                .legend {{
                    margin-top: 14px;
                    font: 12px sans-serif;
                    color: #a3a3a3;
                    line-height: 1.8;
                }}

                .red-text {{
                    color: #f87171;
                }}

                .green-text {{
                    color: #4ade80;
                }}

                @media (max-width: 500px) {{
                    .bit-row {{ gap: 3px; }}
                    .bit-label {{ font-size: 8px; }}
                    .bit-cell {{ padding: 8px 1px; font-size: 18px; }}
                    .bit-position {{ font-size: 8px; }}
                }}
            </style>

            <div class="section-title">
                1. TRANSMITTER · ORIGINAL CODEWORD
            </div>
            <div class="bit-row">{original_cells}</div>

            <div class="section-title">
                2. CHANNEL · RECEIVED CODEWORD
            </div>
            <div class="bit-row">{received_cells}</div>

            <div class="section-title">
                3. RECEIVER · CORRECTED CODEWORD
            </div>
            <div class="bit-row">{corrected_cells}</div>

            <div class="legend">
                <span class="red-text">■ Error introduced</span>
                &nbsp;&nbsp;
                <span class="green-text">■ Bit corrected</span>
                <br>
                Red marks a bit flipped during transmission.
                Green marks a bit changed by the receiver's correction.
            </div>
            """

            components.html(
                html,
                height=410,
                scrolling=False,
            )

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
