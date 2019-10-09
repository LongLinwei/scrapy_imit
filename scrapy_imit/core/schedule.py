from queue import Queue
from hashlib import sha1
import w3lib.url
class Schedule:
    def __init__(self):
        self.queue=Queue()
        self.total_request=0
        self.ins_list=set()
        self.total_repeat_request=0
    def add_request(self,request):
        self.total_request += 1
        if not self.is_repeat(request):
            self.queue.put(request)
        else:
            self.total_repeat_request+=1

    def get_request(self):
        return self.queue.get(block=False)

    def is_repeat(self,request):
        instruct=self._gen_instruct(request)
        if instruct in self.ins_list:
            return True
        else:
            self.ins_list.add(instruct)
            return False
    def _gen_instruct(self,request):
        url=w3lib.url.canonicalize_url(request.url)
        headers=request.headers if request.headers else {}
        headers=sorted(headers,key=lambda x:x[0])
        data=request.data if request.data else {}
        data=sorted(data,key=lambda x:x[0])
        genter=sha1()
        genter.update(url.encode('utf8'))
        genter.update(request.method.encode('utf8'))
        genter.update(str(headers).encode('utf8'))
        genter.update(str(data).encode('utf8'))
        return genter.hexdigest()