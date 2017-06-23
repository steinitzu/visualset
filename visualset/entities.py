

class AttributeRange(object):
    # value_start: float
    # value_end: float
    # duration_seconds: int

    def __init__(self, left: float,
                 right: float, duration_seconds: int):
        self.left = left
        self.right = right
        self.duration_seconds = duration_seconds

    def __iter__(self):
        yield self.left
        yield self.right        

    @property
    def reverse(self):
        """
        Sort order is reverse (descending)
        """
        return self.left > self.right

    def __str__(self):
        return str((self.left, self.right, self.duration_seconds))


class Line(object):
    # attribute_name: str

    def __init__(self, attribute_name, *ranges: AttributeRange):
        self.ranges = ranges
        self.attribute_name = attribute_name

    def __str__(self):
        return '\n'.join([str((p.left, p.right, p.duration_seconds)) for p in self.ranges])

        
