import base64
class Secret():
  def __init___(self):
    self.show = None
  def set_secret(self, word):
    self.show = (base64.b64encode(word.encode('utf-8'))).decode('ascii')
  def decode(self):
    if self.show != None:
      return (base64.b64decode(self.show)).decode('ascii')
    else:
      return "define a secret first!"