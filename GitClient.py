import xlwt
import csv
import requests
import pprint

class GitClient(object):
    def __init__(self):
        self.base_url = 'https://api.github.com/'
        self.userName = ''
        self.password = ''
        self.autorization = False
        self.notAut = ''
        self.exporter = []
        self.toWrite = {}
    def initial(self,name='def',pas='def'):
        self.userName = name if name != 'def' else input('User Name: ')
        self.password = pas if pas != 'def' else input('User password: ')
        self.autorization = True

    def aboutUser(self):
        r = requests.get(self.base_url + 'users/' + self.userName)
        if r.status_code == 200:
            data = ["Username : " + self.userName, "Name : " + str(r.json().get('name')), "Email : " + str(
                r.json().get('email')), "Followers : " + str(r.json().get('followers'))]
        else:
            data = ['Error '+str(r.status_code) +' '+str(r.json()['message'])]
        return data
    def getRepos(self):
        data = []
        elem = {}
        response = requests.get(self.base_url + 'users/' + self.userName + '/repos')
        if response.status_code == 200:
            json = response.json()
            for i in range(len(json)):
                # print(str(i + 1) + ": " + json[i].get('name'))
                elem = {str(i + 1) : json[i].get('name')}
                data.append(elem)
        else:
            elem = {
                '0':'Error '+str(response.status_code) +' '+str(response.json()['message'])
            }
            data.append(elem)

        return data
    def createRep(self,names='def'):
        name = names if names != 'def' else input('Enter repository name: ')
        data = '{"name":"' + name + '"}'
        response = requests.post('https://api.github.com/user/repos', data=data, auth=(self.userName, self.password))
        if response.status_code == 201:
            return "Repository "+ name +" created"
        else:
            return ("Sorry we can't create "+name+" Repository! Error " + str(response.status_code) +" "+str(response.json()['message']))
    def repoInfo(self,names='def'):
        data = []
        elem = {}
        response = requests.get(self.base_url + 'users/' + self.userName + '/repos')
        name = names if names != 'def' else input('Enter repository name: ')
        resCommit = requests.get(self.base_url + 'repos/' + self.userName + '/'+ name +'/commits')
        resBranch = requests.get(self.base_url + 'repos/' + self.userName + '/' + name + '/branches')
        if response.status_code == 200:

            json = response.json()
            for i in range(len(json)):
                if json[i].get('name') == name:
                    jsonr = json[i]
                    commit = resCommit.json()
                    branch = resBranch.json()
                    elem = {
                        "Name " : jsonr.get('name'),
                        "Full name " : jsonr.get('full_name'),
                        "Language " : str(jsonr.get('language')),
                        "Count commits " : str(len(commit)),
                        "Count branches " : str(len(branch)),
                        "Forks count " : str(jsonr.get('forks_count')),
                        "Open issues count " : str(jsonr.get('open_issues_count')),
                        "Size": str(jsonr.get('size')) + " bytes"
                    }
                    data.append(elem)
        else:
            data.append({'Error' : str(response.status_code)+" "+str(response.json()['message'])})
        return  data
    def followers(self):
        followersList = [
        ]
        response = requests.get(self.base_url + 'users/' + self.userName + '/followers')
        if response.status_code == 200:
            json = response.json()
            for i in range(len(json)):
                elem= {
                    'follower': json[i].get('login')
                }
                followersList.append(elem)
        else:
            followersList.append({'Error': str(response.status_code) + " " + str(response.json()['message'])})
        if len(followersList) == 0:
            followersList.append({'follower':'none'})
        return followersList
    def sizeGit(self):
        sizeGit=0
        res = ''
        response = requests.get(self.base_url + 'users/' + self.userName + '/repos')
        if response.status_code == 200:
            json = response.json()
            for i in range(len(json)):
                sized = requests.get(self.base_url + 'repos/' + self.userName + '/' + json[i].get('name'))
                if sized.status_code == 200:
                    sized = sized.json()
                    sizeGit += + float(sized.get('size'))
                else:
                    res = 'Error ' + str(response.status_code)+" "+str(response.json()['message'])
            res = str(sizeGit) + ' bytes'
        else:
            res = 'Error ' + str(response.status_code)+" "+str(response.json()['message'])
        return res
    def prints(self,obj):
        toPrint = {}
        for elem in obj:
            toPrint.update(elem)
        for k in toPrint:
            print(k +": "+toPrint[k])
    def exports(self):
        self.initial()
        saveAs = input('enter format saved (csv or xls)')
        user = [{
            'User': self.userName,
            'Size Git Repositories': self.sizeGit()
        }]
        self.exporter.append(self.getRepos())
        self.exporter.append(self.repoInfo())
        self.exporter.append(self.followers())
        self.exporter.append(user)
        data = self.exporter
        toWrite = {}
        for elem in data:
            if type(elem) == 'dict':
                toWrite.update(elem)
            else:
                for sub in elem:
                    toWrite.update(sub)
        for k in toWrite:
            print(k +": "+toWrite[k])
        name = input('Enter file name: ')
        if saveAs.lower() == 'csv':
            file = open(name+'.csv', 'w')
            writer = csv.writer(file,delimiter=";",quotechar='"')
            writer.writerows(toWrite)
            file.close()
            print('File saved as '+name+'.csv')
        elif saveAs.lower() == 'xls':
            book = xlwt.Workbook()
            sh = book.add_sheet("About")
            for n, k in enumerate(toWrite):
                print(n, k, toWrite[k])
                sh.write(n, 0, k)
                sh.write(n, 1, toWrite[k])
            book.save(name + ".xls")
            print('File saved as ' + name + '.xls')
        else:
            print('Incorrect file sys!!!')



