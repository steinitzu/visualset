import random
from functools import partial

import pytest


@pytest.fixture
def artist_ids():
    return [
        '4I2BJf80C0skQpp1sQmA0h',
        '1qHR9DMfOJQjvWLEfMZQlG',
        '1yAwtBaoHLEDWAnWR87hBT',
        '67ea9eGLXYMsO2eYQRui3w',
        '6DKmuXxXASTF6xaJwcTfjv',
        '36QJpDe2go2KgaRleHCDTp',
        '3zunDAtRDg7kflREzWAhxl',
        '1uR7zoLrSRI8bSL43OZ0GY',
        '5UhutL4dtFLBmnhhbOtIGT',
        '4Ww5mwS7BWYjoZTUIrMHfC',
        '3XHO7cRUPCLOr6jwp8vsx5',
        '1U0FaHAc4fcwQcYEJFgkm9',
        '2RtEDsU4WypWtqxYtYEVcV',
        '7x83XhcMbOTl1UdYsPTuZM',
        '4mw86zm4QZIL8SksdyE6OU',
        '5yV1qdnmxyIYiSFB02wpDj',
        '3vbKDsSS70ZX9D2OcvbZmS',
        '2o1giMbJ0BMwB2O0zU3aDo',
        '776Uo845nYHJpNaStv1Ds4',
        '6Q0gMZJNIebNFFaJeonc11',
        '02uPe16VFxPaiueQsPEDkE',
        '6mMA3DehwLwdvO6YlwUFHk',
        '4UHzJP2iKVf0RhKIv7ZE2l',
        '4yNCQkdoCZc8CAip7SR0C9',
        '6ra4GIOgCZQZMOaUECftGN',
        '6bx5jeXP6LSRVY29adUFdB',
        '1jSaZgaKHmgc7VTgML528r',
        '38zTZcuN7nFvVJ6auhc6V3',
        '74ASZWbe4lXaubB36ztrGX',
        '2kGBy2WHvF0VdZyqiVCkDT',
        '4IDpDJIDfK96HMLD4Tphyl',
        '6UUrUCIZtQeOf8tC0WuzRy',
        '0oSGxfWSnnOXhD2fKuz2Gy',
        '3SCvYjD7RLGzPh0ZtUqw66',
        '22WZ7M8sxp5THdruNY3gXt',
        '1FdwVX3yL8ITuRnTZxetsA',
        '77oD8X9qLXZhpbCjv53l5n',
        '4MOV18YgNAGUBCJi0MIrHw',
        '2i8ynmFv4qgRksyDlBgi6d',
        '1hzfo8twXdOegF3xireCYs',
    ]


def test_most_prominent():
    from visualset.songrepo import most_prominent

    objs = [{'id': i} for i in range(100)]
    
    randint = partial(random.randint, 0)
    
    for i in range(10):
        objs.insert(randint(len(objs)), {'id': 10})

    for i in range(9):
        objs.insert(randint(len(objs)), {'id': 9})

    for i in range(8):
        objs.insert(randint(len(objs)), {'id': 8})

    mp = most_prominent(objs, count=3)
    vals = [i['id'] for i in mp]

    assert vals == [10, 9, 8]
        
