

class FakeScreen:

    def write(self, text):
      print(text)

    def get_visible_size(self):
      return 120, 40