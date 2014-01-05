import os
import re
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

    def get_commit_list(self):
        os.chdir(self._path)

        SEPARATOR = ";;;"
        format_string = ""
        pattern_string = ""

        fields = ["%h", "%s", "%an", "%ad"]
        for f in fields:
            format_string = format_string + f + SEPARATOR
            pattern_string = pattern_string + "(.+)" + SEPARATOR

        git_log = ["git", "log", "--pretty=" + format_string]
        p = Popen(git_log, stdout=PIPE)
        result, err = p.communicate()

        pattern = re.compile(pattern_string)
        return re.findall(pattern, result)

if __name__ == '__main__':
    TEST_PATH = "/home/lee/caf/base"
    gen=Generator(TEST_PATH)
    commit_list = list(gen.get_commit_list())

    final_list = []

    count = 0;
    print "len: ", str(len(commit_list))
    for commit in commit_list:
        cmd = ["git", "show" , commit[0], "--numstat", "--pretty=%h"]
        p = Popen(cmd, stdout=PIPE)
        result, err = p.communicate()

        commit = list(commit)
        pattern = re.compile('\n(\d+)\s+(\d+)\s+(.+)\s')

        commit.append(re.findall(pattern, result))
        final_list.append(commit)
        count = count + len(commit[4])

        #print result

    for commit in final_list:
        print commit
        print "\n"


    print "file count: ", str(count)



