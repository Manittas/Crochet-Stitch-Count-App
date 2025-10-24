class Row:
    def __init__(self, _count = 0):
        self._count = _count
        
    # class methods
    
    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self, value):
        # prevent setting value to negatives or non int values
        if isinstance(value, int) and value >= 0:
            self._count = value
            
    # instance methods
    
    def increment(self):
        self._count += 1
        
    def decrement(self):
        self._count -= 1