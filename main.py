from dataclasses import dataclass
from typing import Any

class InputStream:
    def __init__(self, input: str):
        self.input = input

        self.pos = 0
        self.line = 1
        self.col = 0

    def next(self) -> str:
        char = self.input[self.pos]
        if char == "\n":
            self.line += 1
            self.col = 0
        else:
            self.col += 1
        self.pos += 1
        return char

    def peek(self) -> str:
        return self.input[self.pos]

    def eof(self) -> bool:
        return self.pos >= len(self.input)

    def throw(self, msg: str):
        raise Exception(f"Error: {msg} (line {self.line}, column {self.col})")

@dataclass
class Token:
    type: str
    value: Any 

class Tokenizer:
    def __init__(self, stream: InputStream):
        self.stream = stream

    def is_whitespace(self, ch: str) -> boolean:
        return ch == "\n" || ch == "\t" || ch == " "

    # just to stay consistent
    def is_quote(self, ch: str) -> boolean:
        return ch == '"'

    def is_comment(self, ch: str) -> boolean:
        return ch == "#"

    def is_digit(self, ch: str) -> boolean:
        return ch in "0123456789"

    # well, not really... (due to -)
    def is_letter(self, ch: str) -> boolean:
        return ch in "abcdefghijklmnopqrstuvwxyz-"

    def consume_line(self):
        start = self.stream.line
        while self.stream.line == start:
            self.stream.next()

    def consume_string(self):
        string = ""
        while not is_quote(self.stream.peek()):
            string += self.stream.next()
            if self.stream.eof():
                self.stream.throw("string is not closed")
        return string

    def consume_digit(self):
        digit = 0
        while not self.steam.eof() and is_digit(self.stream.peek()):
            ch = self.stream.next()
            digit = digit * 10 + int(ch)
        return digit

    def consume_

    def next_token(self):
        ch = self.stream.peek()
        if is_comment(ch):
            self.consume_line()
            return None
        elif is_quote(ch):
            return Token(type="str", value=self.consume_string())
        elif is_digit(ch):
            return Token(type="num", value=self.consume_digit())
        elif is_letter(ch):


    def tokenize(self):
        while not self.stream.eof():
            ch = self.stream.peek()
            if is_whitespace(ch):
                self.stream.next()
                continue
            
            token = self.next_token()

