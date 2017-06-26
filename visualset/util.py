from bisect import bisect_left
from numpy.random import uniform
from random import sample
from collections import Counter


def chunked(seq, n):
    chunk = []
    for i in seq:
        chunk.append(i)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def closest_index(seq, x):
    """
    Given list of numbers and a number,
    return the index of the number closest to `x` in list
    """
    pos = bisect_left(seq, x)
    if pos == 0:
        return pos
    if pos == len(seq):
        return pos-1
    before = seq[pos-1]
    after = seq[pos]
    if after - x < x - before:
        return pos
    else:
        return pos-1


def sampled_songs(songs, audio_feature, left_val, right_val, n):
    """
    Sample the given list of songs by the value of given audio feature.
    Attempts to create a uniform distribution from left_val to right_val.

    Args:
        songs: the list of songs (dicts)
        audio_feature(str): name of the audio feature to sample on
        left_val(float): starting value of audio feature
        right_val(float): end value of audio feature
        n(int): number of songs in resulting sample
    Returns:
        Sampled list of songs, sorted in order from left_val to right_val
    """
    if left_val == right_val:
        return sample(songs, n)
    songs = sorted(songs, key=lambda x: x['audio_features'][audio_feature])
    just_numbers = [song['audio_features'][audio_feature] for song in songs]

    reverse = left_val > right_val
    # TODO: use reveerse to choose operator (< | >)
    # Make sure next song isn't equal to the previous, but either more or less than

    uni = sorted(
        uniform(min(left_val, right_val), max(left_val, right_val), n),
        reverse=reverse
    )
    result_songs = []
    for num in uni:
        index = closest_index(just_numbers, num)
        just_numbers.pop(index)
        song = songs.pop(index)
        result_songs.append(song)
    return sorted(
        result_songs,
        key=lambda x: x['audio_features'][audio_feature],
        reverse=reverse
    )


def most_prominent(items, count=20, key='id'):
    """
    From a sequence of dicts yield the `count` most
    prominent items by value of `key`
    """
    items = sorted(items, key=lambda x: x[key])
    item_keys = (item[key] for item in items)
    items_by_key = {item[key]: item for item in items}
    
    counter = Counter(item_keys)

    return (items_by_key[k] for k, v in counter.most_common(count))


def uniquify(items, key='id'):
    """
    From a sequence of dicts, yield each unique item only once.
    Uniqueness of an item is determined by the provided key.

    Args:
        items (sequence): A sequence of dictionaries containing `key`
        key (hashable type): The dictionary key that determines uniqueness
    Returns:
        generator
    """
    seen = set()
    seen_add = seen.add
    for item in items:
        if item[key] in seen:
            continue
        seen_add(item[key])
        yield item
