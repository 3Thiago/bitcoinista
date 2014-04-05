# Install pybitcointools

import urllib
import zipfile
import tarfile
import shutil
import os

def github_download(user, repo, branch):
    print 'Downloading {0}...'.format(repo)
    url = 'https://github.com/{0}/{1}/archive/{2}.zip'.format(user, repo, branch)
    zipname = repo + '.zip'
    urllib.urlretrieve(url, zipname)

    print 'Extracting...'
    z = zipfile.ZipFile(zipname)
    z.extractall()
    os.remove(zipname)
    print 'Done.'
    
    dirname = repo + '-' + branch
    return dirname

def pypi_download(package, version):
    print 'Downloading {0}...'.format(package)
    url = 'https://pypi.python.org/packages/source/{0}/{1}/{1}-{2}.tar.gz'.format(package[0], package, version)
    tarname = package + '.tar.gz'
    urllib.urlretrieve(url, tarname)

    print 'Extracting...'
    t = tarfile.open(tarname)
    t.extractall()
    os.remove(tarname)
    print 'Done.'

    dirname = package + '-' + str(version)
    return dirname

# Download pybitcointools

user = 'christianlundkvist'
repo = 'pybitcointools'
branch = 'purepyhashbackup'
dirname = github_download(user, repo, branch)
if os.path.isdir(repo):
	shutil.rmtree(repo)
shutil.move(dirname+'/bitcoin', './' + repo)
shutil.rmtree(dirname)

# Download slowaes

package = 'slowaes'
version = '0.1a1'
aesfile = 'aes.py'
dirname = pypi_download(package, version)
if os.path.isfile(aesfile):
	os.remove(aesfile)
shutil.move(dirname+'/'+aesfile, './'+aesfile)
shutil.rmtree(dirname)

# Download bitcoinista

user = 'christianlundkvist'
repo = 'bitcoinista'
branch = 'master'
dirname = github_download(user, repo, branch)
if os.path.isdir(repo):
	shutil.rmtree(repo)
shutil.move(dirname+'/'+repo, './' + repo)
shutil.move(dirname+'/bitcoinista.py', './bitcoinista.py')
shutil.rmtree(dirname)
