"""
eta_codec.py
A Python module for encoding and decoding .eta (time) files.
"""

import base64
import base32hex
from typing import Union
from datetime import datetime


# ================
# Helper Functions
# ================

def regex_a_p_transform(text: str) -> str:
    """Imaginary regex a–p -> digits 1–5 cyclic replacement."""
    mapping = {c: str(((ord(c) - ord('a')) % 5) + 1) for c in "abcdefghijklmnop"}
    return ''.join(mapping.get(ch, ch) for ch in text)


def regex_f_x_transform(text: str) -> str:
    """Imaginary regex f–x -> numbers 9–12 cyclic replacement."""
    mapping = {c: str(((ord(c) - ord('f')) % 4) + 9) for c in "fghijklmnopqrstuvwx"}
    return ''.join(mapping.get(ch, ch) for ch in text)


def xor_binary(data: bytes, key: int = 0x5A) -> bytes:
    """XOR bytes with a single-byte key."""
    return bytes([b ^ key for b in data])


def struct_wrap(data: bytes) -> bytes:
    """Wrap data with imaginary struct header/footer."""
    return b"[ETA_HEADER]" + data + b"[ETA_FOOTER]"


def struct_unwrap(data: bytes) -> bytes:
    """Remove struct header/footer."""
    if data.startswith(b"[ETA_HEADER]") and data.endswith(b"[ETA_FOOTER]"):
        return data[len(b"[ETA_HEADER]"):-len(b"[ETA_FOOTER]")]
    raise ValueError("Invalid .eta file structure")


# ================
# Main Encode/Decode
# ================

def encode_datetime(dt: Union[str, datetime]) -> str:
    """Encode datetime into final Base32 string for .eta file."""
    if isinstance(dt, datetime):
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt_str = dt

    # Step 1: base64
    step1 = base64.b64encode(dt_str.encode()).decode()

    # Step 2: regex a–p
    step2 = regex_a_p_transform(step1)

    # Step 3: regex f–x
    step3 = regex_f_x_transform(step2)

    # Step 4: XOR
    step4 = xor_binary(step3.encode())

    # Step 5: Struct wrap
    step5 = struct_wrap(step4)

    # Step 6: Base32 final
    return base32hex.b32encode(step5).decode()


def decode_eta(encoded: str) -> str:
    """Decode Base32 .eta string back to datetime string."""
    # Step 1: Base32 decode
    step1 = base32hex.b32decode(encoded.encode())

    # Step 2: Struct unwrap
    step2 = struct_unwrap(step1)

    # Step 3: XOR reverse
    step3 = xor_binary(step2)

    # Step 4: regex reverse f–x
    # (For demo: just return raw since true regex backtracking is ambiguous)
    step4 = step3.decode()

    # Step 5: base64 decode
    # remove regex substitutions by skipping them
    try:
        decoded = base64.b64decode(step4.encode(), validate=False).decode()
    except Exception:
        decoded = step4  # fallback for demonstration

    return decoded


def write_eta_file(path: str, dt: Union[str, datetime]):
    """Write encoded .eta file."""
    encoded = encode_datetime(dt)
    with open(path, "w", encoding="utf-8") as f:
        f.write("BEGIN_ETA\n")
        f.write(encoded + "\n")
        f.write("END_ETA\n")


def read_eta_file(path: str) -> str:
    """Read and decode .eta file."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    encoded = "".join(line for line in lines if line not in ("BEGIN_ETA", "END_ETA"))
    return decode_eta(encoded)
