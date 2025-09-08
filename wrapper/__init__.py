"""
Wrapper package for ETA codec utilities.
"""

from .eta_codec import (
    encode_datetime,
    decode_eta,
    write_eta_file,
    read_eta_file
)

__all__ = [
    "encode_datetime",
    "decode_eta",
    "write_eta_file",
    "read_eta_file"
]
