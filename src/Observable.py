from ObservableData import ObservableData

class Observable:
    def __init__(self,name):
        self._name = name
        self._observers =[]

    def attach(self,observer):
        self._observers.append(observer)

    def detach(self,observer):
        self._observers.remove(observer)
    
    def notify(self,value):
        for observer in self._observers:
            observer.update(ObservableData(self._name,value))