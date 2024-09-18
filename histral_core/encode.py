import zlib
import base64
import logging as Logger


# Config for custom logging
Logger.basicConfig(
    level=Logger.INFO,
    format="[%(levelname)s] (%(asctime)s) -> %(message)s",
    handlers=[
        Logger.StreamHandler(),
    ],
)


def encode_text(text: str, shouldLog: bool = False) -> str:
    """
    Compress and Encode [text] using `zlib` and `base64`
    **Args**:
        `shouldLog (Boolean)`: _Decide whether function should log reduction
        info or not. Defaults to **False**_
    """

    try:
        compressed = zlib.compress(text.encode())
        encoded = base64.b64encode(compressed).decode()

        # Log info if [shouldLog] is `True`
        if shouldLog:
            original_size = len(text.encode())
            encoded_size = len(encoded.encode())
            reduction_percentage = (
                (original_size - encoded_size) / original_size
            ) * 100

            Logger.info(
                f"INFO: Text compressed and encoded with {reduction_percentage:.2f}% size reduction."
            )

        return encoded
    except Exception as e:
        Logger.error(f"ERROR: Unable to encode text: {e}")
        return text


def decode_text(encoded_text: str) -> str:
    """
    Decode and Decompress [encoded_text] using `base64` and `zlib`
    """

    try:
        # Decode the Base64 string to get the compressed binary data
        compressed_data = base64.b64decode(encoded_text)

        # Decompress the binary data to get the original string
        decompressed = zlib.decompress(compressed_data).decode()

        return decompressed
    except Exception as e:
        Logger.error(f"ERROR: Unable to decode text: {e}")
        return encoded_text
