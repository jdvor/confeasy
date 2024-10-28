from confeasy.cmdline import CommandLine


def test_cmdline():
    args = [
        "--AlphaHorse",
        "2",
        "--Beta",
        "yes",
        "--Flag",
        "--gamma_goat__surplus",
        "-9.67",
        "--BrownSugar__RetailPrice",
        "65.99",
    ]
    sut = CommandLine(args)
    actual = sut.get_configuration_data()
    assert actual["alpha_horse"] == 2
    assert actual["beta"] == "yes"
    assert actual["flag"] == True
    assert actual["gamma_goat.surplus"] == -9.67
    assert actual["brown_sugar.retail_price"] == 65.99
