import pandas as pd

from .sources import SeriesSource


def sources_from_csv(uri, **kwargs):
    """
    Util method to create a collection of sensors from a columnar CSV file
    via Pandas

    :param uri: Location to load CSV from
    :param kwargs: Passthrough args to Pandas
    :return: Dict of SeriesSensor objects keyed to CSV column names
    """
    sources = {}
    df = pd.read_csv(uri, **kwargs)
    for col in df.columns:
        sources[col] = SeriesSource(df[col])
    return sources
