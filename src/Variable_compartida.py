class Variable_compartida():
    def __init__(self,value):
        self._value = value

    def getValue(self):
        return self._value

    def setValue(self,newValue):
        self._value = newValue