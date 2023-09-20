import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
class myStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        new_name = "uploads/mypicdocs_"+str(int(datetime.now().timestamp())) + os.path.splitext(name)[-1]
        return super().get_available_name(new_name, max_length)