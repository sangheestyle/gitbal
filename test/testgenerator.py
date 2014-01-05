import os
import shutil
from subprocess import Popen, PIPE
import unittest
import generator

class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.git_name = "mock_git_repo"
        self.current_dir = os.getcwd()
        self.current_git_path = ""
        git_init = ["git", "init"]
        make_a_file = ["touch", "a.txt"]
        git_add = ["git", "add", "a.txt"]
        git_commit = ["git", "commit", "-m", "'test commit'"]
        commands = [git_init, make_a_file, git_add, git_commit]
        try:
            os.mkdir(self.git_name)
            os.chdir(self.git_name)
            for command in commands:
                p = Popen(command, stdout=PIPE)
                result = p.communicate()
                if result[1] is None:
                    self.current_git_path = os.getcwd()
                else:
                    print result[1]
        except:
            os.chdir(self.current_dir)
            shutil.rmtree(self.git_name)

    def tearDown(self):
        os.chdir(self.current_dir)
        shutil.rmtree(self.git_name)

    def test_get_log(self):
        git_log = ["git", "log"]
        gen = generator.Generator(self.current_git_path)
        p = Popen(git_log, stdout=PIPE)
        result = p.communicate()
        self.assertEqual(gen.get_log(git_log), result[0])

if __name__ == '__main__':
    unittest.main()