from dataclasses import dataclass
from typing import Any
import sys

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

    def is_whitespace(self, ch: str) -> bool:
        return ch == "\n" or ch == "\t" or ch == " "

    # just to stay consistent
    def is_quote(self, ch: str) -> bool:
        return ch == '"'

    def is_comment(self, ch: str) -> bool:
        return ch == "#"

    def is_digit(self, ch: str) -> bool:
        return ch in "0123456789"

    def is_letter(self, ch: str) -> bool:
        return ch in "abcdefghijklmnopqrstuvwxyz"

    def is_keyword(self, word: str) -> bool:
        return word in ("lambda", "if", "then", "else", "true", "false")

    def is_punc(self, ch: str) -> bool:
        return ch in "(),;.[]{}"

    # this is ok, since our compound operators aren't special
    def is_operator(self, ch: str) -> bool:
        return ch in ("+", "-", "/", "*", "=", "!", "==", "!=")

    def consume_line(self):
        start = self.stream.line
        while self.stream.line == start:
            self.stream.next()

    def consume_string(self) -> str:
        string = ""
        # consume start quote
        self.stream.next()
        while not self.is_quote(self.stream.peek()):
            string += self.stream.next()
            if self.stream.eof():
                self.stream.throw("string is not closed")
        # consume end quote
        self.stream.next()
        return string

    def consume_number(self) -> int:
        number = 0
        while not self.stream.eof() and self.is_digit(self.stream.peek()):
            ch = self.stream.next()
            number = number * 10 + int(ch)
        return number 

    # keyword or identifier
    def consume_word(self) -> str:
        valid_ch = lambda ch: ch == "-" or self.is_letter(ch) or self.is_digit(ch)

        word = ""
        while not self.stream.eof() and valid_ch(self.stream.peek()): 
            word += self.stream.next()
        return word 

    def consume_punc(self) -> str:
        return self.stream.next()

    # fine since compound operators can only be made up of operators
    def consume_operator(self) -> str:
        operator = ""
        while not self.stream.eof() and self.is_operator(operator + self.stream.peek()): 
            operator += self.stream.next()
        return operator

    def next_token(self):
        ch = self.stream.peek()
        if self.is_comment(ch):
            self.consume_line()
            return None
        elif self.is_quote(ch):
            return Token(type="str", value=self.consume_string())
        elif self.is_digit(ch):
            return Token(type="num", value=self.consume_number())
        elif self.is_letter(ch):
            word = self.consume_word()
            token_type = "kw" if self.is_keyword(word) else "var"
            return Token(type=token_type, value=word)
        elif self.is_punc(ch):
            return Token(type="punc", value=self.consume_punc()) 
        elif self.is_operator(ch):
            return Token(type="op", value=self.consume_operator()) 
        else:
            self.stream.throw("invalid token")

    def tokenize(self):
        while not self.stream.eof():
            ch = self.stream.peek()
            if self.is_whitespace(ch):
                self.stream.next()
                continue 
            token = self.next_token()
            print(token)


for line in sys.stdin: 
    stream = InputStream(line)
    tokenizer = Tokenizer(stream)
    tokenizer.tokenize()
