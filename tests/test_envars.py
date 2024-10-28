from confeasy.envars import EnvironmentVariables
from dotenv import load_dotenv
from pathlib import Path

env_file = Path(__file__).resolve().parent / "test_envars.env"
if not load_dotenv(dotenv_path=env_file):
    raise EnvironmentError(f"{env_file} is not found or it is empty and no environment variables has been set.")


def test_envars():
    sut = EnvironmentVariables(prefix="MYAPP_")
    actual = sut.get_configuration_data()
    assert "connection_string" in actual
    assert "telemetry.sample_rate" in actual
