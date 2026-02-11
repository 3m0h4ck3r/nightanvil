from gigforge import utils
def test_calc_price():
    assert utils.calc_price(hours=10, rate=10, margin=0.0)==100
