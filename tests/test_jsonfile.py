import confeasy.jsonfile
import pytest
from jsonfile import JsonFile
from pathlib import Path


def test_flatten_json():
    js = {"alpha": 1, "beta": {"gamma": 2, "delta": 3}}
    expected = {"alpha": 1, "beta.gamma": 2, "beta.delta": 3}
    actual = confeasy.jsonfile._flatten_json(js)
    assert expected.keys() == actual.keys()


def test_json_file():
    script_dir = str(Path(__file__).resolve().parent)
    sut = JsonFile(base_dir=script_dir).required("sample1.json").required("sample2.json").optional("non-existent.json")
    actual = sut.get_configuration_data()
    assert len(actual) == 4
    assert "alpha_horse" in actual
    assert "omega_fox" in actual
    assert actual["beta.gamma_goat"] == 10


def test_json_file_when_required_is_missing():
    sut = JsonFile().required("non-existent.json")
    with pytest.raises(ValueError) as ex:
        _ = sut.get_configuration_data()
    assert "non-existent.json" in str(ex.value)
