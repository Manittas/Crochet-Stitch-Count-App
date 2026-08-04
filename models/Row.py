import uuid

class Row:
    def __init__(self, _name, _id = uuid.uuid4().hex, _count = 0, _isCurrent = False):
        self._id = _id
        self._name = _name
        self._count = _count
        self._isCurrent = _isCurrent
        
    # class methods
    # -------------
    
    @property
    def rowId(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def count(self):
        return self._count
    
    @property
    def isCurrent(self):
        return self._isCurrent
    
    
    @rowId.setter
    def rowId(self, newId):
        self._id = newId
    
    @name.setter
    def name(self, newName):
        self._name = newName
            
    @count.setter
    def count(self, value):
        # prevent setting value to negatives or non int values
        if isinstance(value, int) and value >= 0:
            self._count = value
    
    @isCurrent.setter
    def isCurrent(self, isCurrent):
        self._isCurrent = isCurrent
            
    # instance methods
    # ----------------
    
    def increment(self):
        self._count += 1
        
    def decrement(self):
        self._count -= 1
