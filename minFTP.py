#!/usr/bin/python
#
# minFTP
# Copyright(c) 2013 Gabriele Salvatori
# http://www.salvatorigabriele.com
# salvatorigabriele@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import re
import socket
from optparse import OptionParser
from ftplib import FTP


class minFTP:


  def __init__( self, hostname, username, password ):

    self.hostname = hostname
    self.username = username
    self.password = password
    self.ftp = FTP(hostname)
  

  def login ( self ):

    hostname_ip = socket.gethostbyname(self.hostname)
    print "\n"
    print "Trying to connect to %s (IP: %s) on port 21..\n" % (self.hostname, hostname_ip)

    print "[+] CONNECTED \n"

    print "Trying to login in..\n"
    self.ftp.login(self.username,self.password)
    print "[+] DONE \n"

    print "###########################################\n"
    print " minFTP                        \n"
    print " A minimalistic terminal-based FTP client\n"
    print "###########################################\n"
    print 'Type "help" to see the entire list of available commands\n'
  

  def currentdir( self ):

    print "\n"
    print "Now you are in %s" % (self.ftp.pwd())
    print "__________________________\n"

    print "FILES:\n"
    self.ftp.dir()
    print "__________________________\n"
  

  def move( self ):

   
    dir_ = raw_input("Set a directory: ")
    print "\n"

    new_dir = self.ftp.cwd(dir_)
    show = self.ftp.pwd()
    print "Currently you are in %s \n" % (show)


  def show_commands( self ):

    print "COMMANDS:\n"
    print "cd       : Move to a path"
    print "ls       : Show files and directories"
    print "upload   : Upload a file"
    print "download : Download a file"
    print "mkdir    : Create a folder" 
    print "rmdir    : Remove a folder"
    print "rename   : Rename a file/folder"
    print "delete   : Delete a file"
    print "quit     : Quit\n"


  

  def rename ( self ):

    from_ = raw_input('File: ')
    to_ = raw_input('New name: ')

    self.ftp.rename(from_,to_)
  

  def delete ( self ):

    file_ = raw_input('File: ')
    self.ftp.delete(file_)
 

  def mkdir ( self ):

    path = raw_input('Insert folder name: ')
    self.ftp.mkd(path)

  def rmdir ( self ):

    path = raw_input('Which folder you want to delete?: ')
    self.ftp.rmd(path)
  

  def download ( self ):

    filename = raw_input('File: ')
    file_ = open(filename,'wb')
    self.ftp.retrbinary('RETR %s' % filename, file_.write)
    file_.close()


  def upload ( self ):

    path = raw_input('Path: ')
    filename = raw_input('Filename: ')
    file_ = os.path.join(path,filename)
    self.ftp.storbinary('STOR %s' % filename, open(file_, 'rb'))
  

  def commandline( self ):

    commands = {'cd'      : self.move,
                'ls'      : self.currentdir,
                'mkdir'   : self.mkdir,
                'upload'  : self.upload,
                'download': self.download,
                'rmdir'   : self.rmdir,
                'rename'  : self.rename,
                'delete'  : self.delete,
                'help'    : self.show_commands}

    cont = True

    while ( cont ):
      selection = raw_input('> ')
      if selection == 'quit':
        cont = False
      elif selection in commands.keys():
        commands[selection]()
      else:
        print '[-] ERROR: wrong command. Type "help" to see the entire list of available commands'
  

 
if __name__ == '__main__':


  usage = 'Usage: python minFTP.py -h "hostname" -u "username" -p "password"'
  parser = OptionParser(usage, add_help_option = False)

  parser.add_option("-h", "--host", dest="hostname")
  parser.add_option("-u", "--user", dest="username")
  parser.add_option("-p", "--pass", dest="password")


  (op, args) = parser.parse_args()

  object_ = minFTP(op.hostname,op.username,op.password)
  
  ###  LOGIN ###
  object_.login()
  ###         ###

  ### CURR. DIR ###
  object_.currentdir()
  ###           ###

  ### COMM. LINE ###
  object_.commandline()
  ###           ###




