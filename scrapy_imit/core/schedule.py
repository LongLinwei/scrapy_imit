from queue import Queue
class Schedule:
    def __init__(self):
        self.queue=Queue()
        self.total_request=0
    def add_request(self,request):
        self.queue.put(request)
        self.total_request+=1

    def get_request(self):
        return self.queue.get()

    def rm_repeat(self):
        pass