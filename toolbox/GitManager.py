import os,sys,logging
import subprocess

class GitManager:
  def __init__(self,gitpath):
    self.gitpath = gitpath
    os.chdir(gitpath)
  
  def commit(self,content, comment):
    PIPE = subprocess.PIPE
    process = subprocess.Popen(['git', 'add', content], stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate() 
    logging.info("git add: "+stdoutput)
    process = subprocess.Popen(['git', 'commit', '-m', comment], stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()
    logging.info("git commit: "+stdoutput)    
    
  

