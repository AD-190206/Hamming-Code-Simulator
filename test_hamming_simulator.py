import unittest

from hamming_simulator import (
    encode_hamming,
    display_codeword,
    transmit,
    receive,
    validate_binary,
)


class TestHammingSimulator(unittest.TestCase):

    def test_reference_encoding(self):
        codeword = encode_hamming("1011")
        self.assertEqual(display_codeword(codeword), "1100110")

    def test_normal_transmission(self):
        codeword = encode_hamming("1011")
        result = receive(transmit(codeword))

        self.assertEqual(result["syndrome"], 0)
        self.assertEqual(result["recovered_data"], "1011")

    def test_every_single_bit_position(self):
        data = "1011"
        codeword = encode_hamming(data)
        length = len(codeword) - 1

        for position in range(1, length + 1):
            with self.subTest(position=position):
                received = transmit(codeword, [position])
                result = receive(received)

                self.assertEqual(
                    result["syndrome"], position
                )
                self.assertEqual(
                    result["recovered_data"], data
                )
                self.assertEqual(
                    result["corrected_codeword"],
                    display_codeword(codeword),
                )

    def test_invalid_binary_input(self):
        for data in ("", "1021", "10a1"):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    validate_binary(data)

    def test_invalid_error_positions(self):
        codeword = encode_hamming("1011")
        length = len(codeword) - 1

        for position in (0, length + 1):
            with self.subTest(position=position):
                with self.assertRaises(ValueError):
                    transmit(codeword, [position])

    
    def test_multiple_input_lengths(self):
        test_inputs = [
            "1",
            "10",
            "1011",
            "10101010",
            "110101101011",
        ]

        for data in test_inputs:
            with self.subTest(data=data):
                codeword = encode_hamming(data)
                result = receive(transmit(codeword))

                self.assertEqual(
                    result["syndrome"], 0
                )
                self.assertEqual(
                    result["recovered_data"], data
                )

    def test_single_bit_correction_across_inputs(self):
        test_inputs = [
            "1",
            "10",
            "1011",
            "10101010",
            "110101101011",
        ]

        for data in test_inputs:
            codeword = encode_hamming(data)
            expected_codeword = display_codeword(codeword)
            length = len(codeword) - 1

            for position in range(1, length + 1):
                with self.subTest(
                    data=data, position=position
                ):
                    received_bits = transmit(
                        codeword, [position]
                    )
                    result = receive(received_bits)

                    self.assertEqual(
                        result["syndrome"], position
                    )
                    self.assertEqual(
                        result["recovered_data"], data
                    )
                    self.assertEqual(
                        result["corrected_codeword"],
                        expected_codeword,
                    )
    
    def test_two_bit_error_experiment(self):
        data = "1011"
        codeword = encode_hamming(data)

        # Flip two different bit positions.
        received_bits = transmit(codeword, [1, 2])
        result = receive(received_bits)

        print("\nTwo-bit error experiment")
        print("Original:", display_codeword(codeword))
        print("Received:", display_codeword(received_bits))
        print("Syndrome:", result["syndrome"])
        print("Corrected:", result["corrected_codeword"])
        print("Recovered:", result["recovered_data"])

if __name__ == "__main__":
    unittest.main()
