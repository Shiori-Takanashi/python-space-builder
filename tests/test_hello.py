# test_hello.py
from code.hello import hello

def test_hello_returns_expected_message():
    assert hello("Alice") == "Hello, Alice!"
