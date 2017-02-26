from cmd import Cmd
from GitClient import GitClient

class CmdGit(Cmd):
    def do_exit(self,line):
        'exit programm'
        exit()
    def do_init(self,line):
        'Initial auth data user name and password'
        s.initial()
    def do_me(self,line):
        'information about User'
        data = s.aboutUser()
        for i in range(len(data)):
            print(data[i])
    def do_ls(self,line):
        'Get all User repositiries'
        s.prints(s.getRepos())
    def do_create(self, line):
        'Create new repositories'
        e = s.createRep()
        print(e)
    def do_aboutRepos(self, line):
        'Information repository'
        s.prints(s.repoInfo())
    def do_followers(self,line):
        'Information about followers'
        s.prints(s.followers())
    def do_size(self,line):
        'Size of all repositories ( size )'
        print(s.sizeGit())
    def do_save(self,line):
        'Save information about Git (Need login)'
        s.exports()



if __name__ == '__main__':
    s = GitClient()
    cm = CmdGit()
    cm.cmdloop(intro="First command must be 'init' ")