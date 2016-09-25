class Logic(object):


    def __init__(self, objects = None):
        self.objects = objects or []

    def clear_all(self):
        self.objects = []
