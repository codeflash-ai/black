# Copyright 2004-2005 Elemental Security, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Safely evaluate Python string literals without using eval()."""

import re

simple_escapes: dict[str, str] = {
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "'": "'",
    '"': '"',
    "\\": "\\",
}


def escape(m: re.Match[str]) -> str:
    tail = m.group(1)
    first_char = tail[0]
    if first_char in simple_escapes:
        return simple_escapes[first_char]

    if first_char == "x":
        hexes = tail[1:]
        if len(hexes) < 2:
            raise ValueError(f"invalid hex string escape ('\\{tail}')")
        try:
            return chr(int(hexes, 16))
        except ValueError:
            raise ValueError(f"invalid hex string escape ('\\{tail}')") from None
    else:
        try:
            return chr(int(tail, 8))
        except ValueError:
            raise ValueError(f"invalid octal string escape ('\\{tail}')") from None


def evalString(s: str) -> str:
    q = s[0]
    if s.startswith(q * 3):
        q *= 3
    assert s.endswith(q), repr(s[-len(q) :])
    assert len(s) >= 2 * len(q)
    s = s[len(q) : -len(q)]
    return re.sub(r"\\([\'\"\\abfnrtv]|x[0-9A-Fa-f]{0,2}|[0-7]{1,3})", escape, s)


def test() -> None:
    for i in range(256):
        c = chr(i)
        s = repr(c)
        e = evalString(s)
        if e != c:
            print(i, c, s, e)


if __name__ == "__main__":
    test()
