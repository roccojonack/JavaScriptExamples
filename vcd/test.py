import io
from vcd.reader import TokenKind, tokenize
vcd = b"$date today $end $timescale 1 ns $end"
# open(path, 'rb')
tokens = tokenize(io.BytesIO(vcd))
token = next(tokens)
assert token.kind is TokenKind.DATE
assert token.date == 'today'
token = next(tokens)
assert token.kind is TokenKind.TIMESCALE
assert token.timescale.magnitude.value == 1
assert token.timescale.unit.value == 'ps'