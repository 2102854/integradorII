class BusinessException(Exception):
    """
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(str(self.value))
    
    # __str__ is to print() the value
    def __str__(self):
        return(repr(self.value))
    
    #def __init__(self, salary, message="Salary is not in (5000, 15000) range"):
    #    self.salary = salary
    #    self.message = message
    #    super().__init__(self.message)
    """
    pass