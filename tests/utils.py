import itertools


def runs_of_ones_list(bits):
    """
    Util method to count up runs of ones in a sample, shamelessly
    borrowed from
    https://stackoverflow.com/a/1066838/773376
    :param bits List of 0/1 values to count run groups of 1s
    :return: List of counts for 1 value run groups in bits
    """
    return [sum(g) for b, g in itertools.groupby(bits) if b]
