import confeasy
import pytest
from tomlfile import TomlFile
from pathlib import Path


def test_toml_file():
    script_dir = str(Path(__file__).resolve().parent)
    sut = TomlFile(base_dir=script_dir).required("sample1.toml").required("sample2.toml").optional("non-existent.toml")
    actual = sut.get_configuration_data()
    assert len(actual) == 4
    assert "alpha_horse" in actual
    assert "omega_fox" in actual
    assert actual["beta.gamma_goat"] == 10


def test_toml_file_when_required_is_missing():
    sut = TomlFile().required("non-existent.toml")
    with pytest.raises(ValueError) as ex:
        _ = sut.get_configuration_data()
    assert "non-existent.toml" in str(ex.value)
