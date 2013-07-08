#!/usr/bin/python

import socket
import maya.cmds as cmds
import os
import time
import sys

def start(ip,port):
    addr= ip+':'+str(port)

    
    try:
        cmds.commandPort(n=addr,sourceType='python')
        print 'opening... '+addr
    except:
        print 'error creating socket on:'
        print addr

    status = cmds.commandPort(addr,q=True)


    return status

def stop(ip,port):
    addr= ip+':'+str(port)
    try:
        cmds.commandPort(n=addr,close=True)
        print 'closing... '+addr
    except:
        print 'no open sockets'


def send_to_zbrush(host, port):

    env = '$ZDOCS'
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.delete(ch=True)
    objs = cmds.ls(selection=True)

    if objs:

        for obj in objs:
            cmds.select(cl=True)
            cmds.select(obj)
            print obj
            print 'Maya >> ZBrush'
            print host+':'+port
            name = os.path.relpath(obj + '.ma')
            ascii_file = os.path.join(env, name)
            print ascii_file
            try:
                os.remove(os.path.expandvars(ascii_file))
            except:
                pass

            cmds.file(  ascii_file,
                        force=True,
                        options="v=0",
                        type="mayaAscii",
                        exportSelected=True)
        time.sleep(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.send('open|' + ':'.join(objs))
        print ('open|' + ':'.join(objs))
        s.close()

        ch_cmds = 'chmod 777 '+os.path.expandvars(env)+'/*'
        os.system(ch_cmds)

    else: 
        print 'Select an object'