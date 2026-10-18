# Hamming Code-Based Data Communication Simulator

## 1. Project Overview

The Hamming Code-Based Data Communication Simulator is a Python
mini-project developed for the Computer Networks Laboratory.

It demonstrates how parity bits are used to detect and correct
single-bit errors during data transmission.

The project includes a Python-based Hamming code implementation
and a Streamlit web interface.

## 2. Objectives

- Encode binary data using Hamming code.
- Generate parity bits using even parity.
- Simulate correct and erroneous transmission.
- Detect a single-bit error using the syndrome.
- Correct the detected single-bit error.
- Recover the original binary data.

## 3. Technologies Used

- Python 3
- Streamlit
- Visual Studio Code

## 4. Project Structure

hamming_code_simulator/
├── hamming_simulator.py
├── app.py
├── requirements.txt
└── README.md

## 5. Features

1. Accepts binary data from the user.
2. Generates a Hamming codeword.
3. Supports normal transmission.
4. Allows the user to introduce a single-bit error.
5. Calculates the receiver syndrome.
6. Displays the error position.
7. Corrects a single-bit error.
8. Displays the recovered data.

## 6. Installation and Execution

### Step 1: Open the project folder

Open the hamming_code_simulator folder in Visual Studio Code.

### Step 2: Create a virtual environment (recommended)

Windows:

    python -m venv .venv
    .venv\Scripts\activate

macOS/Linux:

    python3 -m venv .venv
    source .venv/bin/activate

### Step 3: Install the dependency

    pip install -r requirements.txt

### Step 4: Run the web application

    streamlit run app.py

A local web address will be displayed in the terminal.
Open that address in your browser.

### Step 5: Run the command-line version (optional)

    python hamming_simulator.py

## 7. Working Principle

1. The sender enters binary data.
2. The encoder calculates the required parity bits.
3. The codeword is transmitted through a simulated channel.
4. An optional bit error is introduced.
5. The receiver recalculates the parity checks.
6. The syndrome identifies the position of a single-bit error.
7. The receiver corrects the bit and extracts the original data.

## 8. Test Cases

### Test Case 1: Correct Transmission

Input data: 1011
Expected codeword: 1100110
Expected syndrome: 0
Recovered data: 1011

### Test Case 2: Single-Bit Error

Input data: 1011
Original codeword: 1100110
Flipped bit position: 6 (from the right)
Received codeword: 1000110
Expected syndrome: 6
Corrected codeword: 1100110
Recovered data: 1011

## 9. Limitations

- Basic Hamming code corrects single-bit errors.
- Arbitrary multiple-bit errors are not reliably handled.
- Transmission is simulated locally; no real network connection
  is established.
- The implementation uses even parity.

## 10. Conclusion

The project demonstrates the use of Hamming code in data
communication. It shows how parity bits, syndrome calculation,
and bit correction help improve the reliability of transmitted
binary data.
