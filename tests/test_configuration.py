from __future__ import annotations
from confeasy import Builder
from confeasy.jsonfile import JsonFile
from confeasy.cmdline import CommandLine
from pathlib import Path


def test_one():
    script_dir = str(Path(__file__).resolve().parent)
    args = [
        "--beta",
        "250",
    ]
    builder = Builder().add_source(JsonFile(script_dir).required("sample3.json")).add_source(CommandLine(args))
    config = builder.build()
    alpha = config.get_value("alpha")
    beta = config.get_value("beta")
    assert alpha == "yes"
    assert beta == 250


def test_two():
    builder = Builder().add_data(
        {
            "delta.is_enabled": True,
            "delta.epsilon.increment": 10,
            "delta.epsilon.theta.engine_ratio": 2.57,
            "delta.epsilon.theta.retail_price": "89.99",
            "else.whatever": "lorem ipsum",
        }
    )
    config = builder.build()
    delta = config.bind(Delta(), prefix="delta")
    assert delta.is_enabled == True
    assert delta.epsilon.increment == 10
    assert delta.epsilon.theta.engine_ratio == 2.57
    assert delta.epsilon.theta.retail_price == 89.99


class Delta:
    def __init__(self):
        self.is_enabled: bool = False
        self.epsilon: Epsilon = Epsilon()


class Epsilon:
    def __init__(self):
        self.increment: int = 1
        self.theta: Theta = Theta()


class Theta:
    def __init__(self):
        self.engine_ratio: float = 0.0
        self.retail_price: float = 0.0
