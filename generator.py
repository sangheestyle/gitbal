import os
from subprocess import Popen, PIPE

class Generator:

    def __init__(self, path):
        if os.path.exists(path):
            self._path = path
        else:
            print "invalid path, please check the path"

    def get_log(self, query):
        os.chdir(self._path)
        git_log = ["git", "log"]
        p = Popen(git_log, stdout=PIPE)
        result = p.communicate()
        return result[0]