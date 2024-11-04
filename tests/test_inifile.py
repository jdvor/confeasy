import pytest
from inifile import IniFile
from pathlib import Path


def test_ini_file():
    script_dir = str(Path(__file__).resolve().parent)
    sut = IniFile(base_dir=script_dir).required("sample1.ini").required("sample2.ini").optional("non-existent.ini")
    actual = sut.get_configuration_data()
    assert len(actual) == 4
    assert "alpha_horse" in actual
    assert "omega_fox" in actual
    assert actual["beta.gamma_goat"] == "10"


def test_ini_file_when_required_is_missing():
    sut = IniFile().required("non-existent.ini")
    with pytest.raises(ValueError) as ex:
        _ = sut.get_configuration_data()
    assert "non-existent.ini" in str(ex.value)
