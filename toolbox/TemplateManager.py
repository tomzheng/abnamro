import sys,logging

class TemplateManager:
  logging.basicConfig(stream=sys.stderr, level=logging.INFO)

  def append_file_if_notfound(self, filename,ignorekey,content):
    with open (filename, "r+") as f:
      for line in f:
        if ignorekey in line:
          logging.info("Append action is ingored because setting exists: "+ignorekey)			
          break
      else:
          f.write(content)

  def insert_file_if_notfound(self, filename,ignorekey,content,matchkey):
    inputfile = open(filename, 'r').readlines()
    found = False
    for line in inputfile:
      if ignorekey in line:
        found = True
        logging.info("Insert action is ignored because setting exists: "+ignorekey)
        break
    if not found:
      writefile = open(filename,'w')
      for line in inputfile:
        writefile.write(line)
        if matchkey in line:
          writefile.write(content)
      writefile.close()

