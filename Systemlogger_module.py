
"""
Helper module with log writer

Autohor: Peder I. Dahl
Date: 15 August 2022
"""

class logger():
    """Class to handle logging to screen and file

    Helper class to add logging information during program flow.
    The class holds a list of strings that is printed to screen
    and file with the method addp(). 
    """
    
    def __init__(self, fn, s = ""):
        self.fn = fn # Log file name
        self.s = [s] # Array of log strings
        self.p = 0   # Points to last printed element in self.s

    def add(self, s):
        self.s.append(s)

    def addp(self, s):
        self.s.append(s)
        for i in range(self.p, len(self.s)):
            print(self.s[i])
        with open(self.fn, "a") as fh:
            fh.writelines(e + "\n" for e in self.s[self.p:])
        self.p = len(self.s)
        
    def __str__(self):
        return '\n'.join(self.s)


if __name__ == "__main__":
    log = logger("test.log")
    log.add("First log line")
    log.addp("Second log line")
    print(log)