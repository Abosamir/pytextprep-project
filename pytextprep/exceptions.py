# PyTextPrepError, UnknownStepError, InvalidStepParamsError

class PyTextPrepError(Exception):
    pass

class UnknownStepError(PyTextPrepError):
    pass

class InvalidStepParamsError(PyTextPrepError):
    pass