# Install pybitcointools

import urllib
import zipfile
import shutil
import console
import os

def github_download(user, repo, branch):
    print 'Downloading {0}...'.format(repo)
    url = 'https://github.com/' + user + '/' + repo + '/archive/' + branch + '.zip'
    zipname = repo + '.zip'
    urllib.urlretrieve(url, zipname)

    print 'Extracting...'
    z = zipfile.ZipFile(zipname)
    z.extractall()
    os.remove(zipname)
    print 'Done.'
    
user = 'christianlundkvist'
repo = 'pybitcointools'
branch = 'purepyhashbackup'

github_download(user, repo, branch)
dirname = repo + '-' + branch
if os.path.isdir(repo):
	shutil.rmtree(repo)
shutil.move(dirname+'/bitcoin', './' + repo)
shutil.rmtree(dirname)

user = 'christianlundkvist'
repo = 'bitcoinista'
branch = 'master'

github_download(user, repo, branch)
dirname = repo + '-' + branch
if os.path.isdir(repo):
	shutil.rmtree(repo)
shutil.move(dirname+'/'+repo, './' + repo)
shutil.move(dirname+'/bitcoinista.py', './bitcoinista.py')
shutil.rmtree(dirname)

