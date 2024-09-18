import unittest

from unittest.mock import patch
from histral_core.encode import encode_text, decode_text


class TestEncode(unittest.TestCase):
    """
    Unit tests for `core.encode` module
    """
    
    def test_encode_and_decoding_success(self):
        text = "Hello, World!"
        encoded = encode_text(text)
        
        decoded = decode_text(encoded)
        self.assertEqual(text, decoded)
        
    def test_encode_text_with_logging(self):
        text = "Logging Test"
        with patch('core.encode.Logger.info') as mock_log:
            encode_text(text, shouldLog=True)
            self.assertTrue(mock_log.called)
            log_message = mock_log.call_args[0][0]
            self.assertIn("Text compressed and encoded with", log_message)
    
    def test_encode_text_failure(self):
        with patch('core.encode.zlib.compress', side_effect=Exception("Compression error")):
            encoded = encode_text("Hello, World!")
            self.assertEqual("Hello, World!", encoded)
    
    def test_decode_text_failure(self):
        with patch('core.encode.base64.b64decode', side_effect=Exception("Decoding error")):
            decoded = decode_text("invalid_encoded_text")
            self.assertEqual("invalid_encoded_text", decoded)


if __name__ == '__main__':
    unittest.main()
