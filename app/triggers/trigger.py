class Trigger:
    def __init__(self, message):
        self.message = message

    def is_math_expression(self):
        s = self.message
        s = s.rstrip()  # Remove trailing whitespace
        if "*" in s or "/" in s or "+" in s or "-" in s:
            try:
                eval(s)
                return True
            except (SyntaxError, NameError, TypeError, ZeroDivisionError , ValueError, AttributeError, IndexError, KeyError, NotImplementedError):
                return False
        else:
            return False
    