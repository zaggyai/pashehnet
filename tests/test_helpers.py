from pashehnet.sensors.helpers import sources_from_csv


def test_sources_from_csv():
    sources = sources_from_csv(
        'tests/sensors.csv',
        usecols=['s1', 's3'],
        dtype=int
    )
    expected = [
        [1, 3],
        [2, 4],
        [3, 5],
        [4, 6],
        [5, 7],
        [6, 8],
        [7, 9],
        [8, 0],
        [1, 3],
        [2, 4]
    ]
    samples = [
        [next(sources[c]) for c in sources.keys()]
        for _ in range(len(expected))
    ]
    assert expected == samples
