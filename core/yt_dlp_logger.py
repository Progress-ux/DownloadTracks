class NoWarningLogger:
   def __init__(self, print=None):
      self.print = print

   def debug(self, msg):
      pass
   def warning(self, msg):
      pass
   def error(self, msg):
      print(msg)