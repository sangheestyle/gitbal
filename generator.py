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

    def add_modified_files_info(self, commit_list):
        result_list = []

        for commit in commit_list:
            cmd = ["git", "show" , commit[0], "--numstat"]
            p = Popen(cmd, stdout=PIPE)
            result, err = p.communicate()
            pattern = re.compile('\n(\d+)\s+(\d+)\s+(.+)\s')
            commit = list(commit)
            commit.append(re.findall(pattern, result))

            result_list.append(commit)
        return result_list

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
        commit_list = re.findall(pattern, result)

        return self.add_modified_files_info(commit_list)

    def print_commits_info(self, commit_list):
        print "Total Commit Count: " + str(len(commit_list)) + "\n"

        for commit in commit_list:
            print "[ ", commit[0], " / ", commit[1], " / ", commit[2], " / ", commit[3], " ]"
            for file in commit[4]:
                print file
            print "--------------------------------------------------------------------------------------------------\n"

if __name__ == '__main__':
    TEST_GIT_PATH = "/home/lee/caf/base"

    gen=Generator(TEST_GIT_PATH)
    commit_list = gen.get_commit_list()

    #print commit_list
    gen.print_commits_info(commit_list)








