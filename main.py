from flask import Flask, render_template, abort, request , views
import requests
from GitClient import GitClient

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html',
        title = 'Home')

@app.route('/', methods=['POST'])
def user_info():
    g = GitClient()
    user = request.values.get('username', None)
    password = request.values.get('password', None)
    cname = request.values.get('create', None)
    repname = request.values.get('repname', None)
    g.initial(user,password)
    if g.autorization:
        if cname != None:
            print('yes',cname)
            cr = g.createRep(cname)
        else:
            cr = 'Not name'
        repos = g.getRepos()
        abUser = g.aboutUser()
        repinfo = ''
        if repname != None:
            repinfo = g.repoInfo(repname)
        else:
            repinfo = g.repoInfo(repos[0])
        return render_template('index.html',abUser = abUser, repos = repos, autorize = g.autorization, repinfo=repinfo,
                               repname=repname,  create = cr ,crname = cname)
    else:
        return render_template('index.html',errorL ="Some errors")

if __name__ == '__main__':
    app.run(debug=True)
