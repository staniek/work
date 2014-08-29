# -*- coding: utf-8 -*-
import os,sys
import Editor
import Lokalize
import subprocess
from opensrc_list import mapSrc

print Editor.currentFile()
editor=Editor
globals()['test']='sssss'
lll=['sss']

ourPath=([p for p in sys.path if p.endswith('/scripts/lokalize')]+[''])[0]

def srcFileOpenRequested(filename, line):
    try: Editor.setSrcFileOpenRequestAccepted(True)
    except: print 'your lokalize needs update ;)'

    if not editor.isValid() or editor.currentFile()=='': return

    import Kross
    forms = Kross.module("forms")
    print filename

    (path, pofilename)=os.path.split(Editor.currentFile())
    (package, ext)=os.path.splitext(pofilename)
    (upperPath, module)=os.path.split(path)
    if module.startswith('extragear-'):
        module=module.replace('extragear-','../extragear/')
    elif module.startswith('playground-'):
        module=module.replace('playground-','../playground/')
    elif module=='kdebase':
        trySubmodules=['workspace','apps','runtime']
        for s in trySubmodules:
            if os.path.exists(ourPath+'/../../../KDE/kdebase/'+s+'/'+package):
                module=module+'/'+s
                print module
                break
    if package.startswith('desktop_'):
        while 1:
            try: package=package[package.index('_')+1:]
            except: break
    KdeTrunkPath=os.path.normpath(ourPath+'/../../../')
    mapSrcSuggest = mapSrc.get(package, '---')

    srcFilePath = subprocess.check_output(["/bin/bash", "-c", "/bin/find "
                                           + os.getenv("HOME")+"/dev/src/calligra/ | grep "
                                           + filename + "$"]).split('\n')[0]
    #srcFilePath = os.getenv("HOME")+"/dev/src/calligra/kexi/" + filename
    if len(srcFilePath):
        #os.system('kdialog --msgbox "'+srcFilePath + '%d' % line + '"')
        subprocess.call(['/usr/bin/kate', '-u', srcFilePath, '--line', '%d' % line])
        print 'kate -u '+srcFilePath+(' --line %d &' % line)
    else:
        print "couldn't find. searched in:",
        print tryList
        answer=forms.showMessageBox("QuestionYesNo", "Could not find source file", "Searched in:\n"+'\n'.join(tryList)+"""
Also searched using 'locate' command.

Would you like to initiate websearch (using lxr.kde.org)?
        """)
        if answer=='Yes':
            os.system("kfmclient openURL 'http://lxr.kde.org/search?filestring=%s&string='" % filename)

