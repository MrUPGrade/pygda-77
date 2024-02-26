from api.helpers import paging_params


def test_paging_params():
    result = paging_params(11, 14)

    assert isinstance(result, dict)
    assert result['offset'] == 11
    assert result['limit'] == 14


def test_paging_params_defaults():
    result = paging_params()

    assert isinstance(result, dict)
    assert result['offset'] == 0
    assert result['limit'] == 10
