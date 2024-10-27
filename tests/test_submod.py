import io
import os

from dotenv import load_dotenv

from module1.submod import hello_world


load_dotenv()


def test_sample():
    hello_world()
    assert True
