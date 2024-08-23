from falken_trace.utils import flatten_dict


def test_flatten_dict() -> None:
    # given
    data = {
        "1": {"2": 3},
        "4": True,
        "5": {
            "6": {
                "7": ["8"],
            }
        },
    }

    # when
    flat = flatten_dict(data)

    # then
    assert flat == {
        "1.2": "3",
        "4": "True",
        "5.6.7": "['8']",
    }
