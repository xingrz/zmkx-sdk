from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint


def encode(message):
    """Encode a protobuf message as a delimited message."""
    serialized = message.SerializeToString()
    delimiters = []
    _EncodeVarint(delimiters.append, len(serialized))
    return b''.join(delimiters) + serialized


def decode(buffer):
    """Decode a delimited message into a protobuf message."""
    (size, pos) = _DecodeVarint32(buffer, 0)
    msg = buffer[pos:pos + size]
    return bytes(msg)
