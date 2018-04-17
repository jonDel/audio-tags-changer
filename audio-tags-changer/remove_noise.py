#!/usr/bin/python
#coding: utf-8
import os
from loggers import Loggers
import subprocess


# Configurando um handler de log
mlog = Loggers('mp3Tags')
mlog.set_log_level('ERROR')

def sox_wrapp_nonoise(infile, outfile, **kwargs):
    def_args = {'noise_profile':'noise_profile_file',
                'profile_value':'0.31'
                }
    def_args.update(kwargs)
    if infile == outfile:
        outfile = outfile+'_OUT.mp3'
    cmd= str('sox '+ '"'+infile+'"'+' "'+outfile+'" '+ 'noisered ' +def_args['noise_profile']\
         +' '+ def_args['profile_value'])
    rem_noise = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = rem_noise.communicate()
    if not rem_noise.returncode:
        cmd= str('mv '+ '"'+outfile+'" ' + '"'+infile+'"')
        rem_noise = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = rem_noise.communicate()
        if rem_noise.returncode:
            print (err)
            return False
    else:
        print (err)
        return False
    return bool(not(rem_noise.returncode))


def getFilesNames(dirPath, recursive=True, fileFilter=''):
    ''' 
    Description: search for all the file paths in folder
    Parameters:
        dirPath: folder path to be scanned
        recursive: if True, scan recursivelly all subfolders of folder (default: True)
        fileFilter: if not empty string, filter files by its extension (Ex: avi returns only *.avi files). Default: ''
    Return:
        filesList: list containing all the files path
    '''
    if recursive:
        filesList = [os.path.join(dirAbsPath, f) for dirAbsPath, dn, filenames in os.walk(dirPath) for f in filenames if f.endswith(fileFilter)]
    else:
        filesList =[os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath) if fileName.endswith(fileFilter) if os.path.isfile(os.path.join(dirPath,fileName))]
    return filesList

def remove_noise(folder, noise_profile_file='noise_profile_file'):
    '''
    Description: remove noise from mp3 files
    Parameters
        folder: folder path
    '''
    for mfile in getFilesNames(folder):
        print ('Removing noise from file {} ...'.format(mfile))
        ret = sox_wrapp_nonoise(mfile, mfile, noise_profile=noise_profile_file)
        if not ret:
            print ("Could't remove noise from file {}".format(mfile))

