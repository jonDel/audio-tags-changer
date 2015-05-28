#!/usr/bin/python
#coding: utf-8
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from mutagen.m4a import M4A
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.monkeysaudio import MonkeysAudio
from mutagen.aac import AAC
from mutagen.id3 import ID3, TPE1, ID3NoHeaderError
import re
import os
from loggers import loggers


# All suported files extensions
audiofileDict = {'mp3':'EasyID3','mp4':'MP4','flac':'FLAC', 'm4a':'M4A','ogg':'OggVorbis','ape':'MonkeysAudio', 'aac':'AAC' }

# Configurando um handler de log
mlog = loggers('mp3Tags')
mlog.setLogLevel('ERROR')

def getFilesNames(dirPath, recursive=True, flag=''):
	''' 
	Description: search for all the file paths in folder
	Parâmetros:
	Parameters:
		dirPath: folder path to be scanned
		recursive: if True, scan recursivelly all subfolders of folder (default: True)
		flag: se não for vazia, retorna apenas os arquivos com essa terminação(default: '')
		filter: if not empty string, filter files by its extension (Ex: avi returns only *.avi files). Default: ''
	Return:
		filesList: list containing all the files path
	'''
	if recursive:
		filesList = [os.path.join(dirAbsPath, f) for dirAbsPath, dn, filenames in os.walk(dirPath) for f in filenames if f.endswith(flag)]
	else:
		filesList =[os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath) if fileName.endswith(flag) if os.path.isfile(os.path.join(dirPath,fileName))]
	return filesList

def changeTagInMediaFiles(folder,tag,tagInfo):
	''' 
	Description: change tags of music files supported recursivelly in the folder path
	Parameters
		folder: folder path
		tag:    tag name (ex: artist)
		tagInfo: tag string (ex: Magnitude9)
	'''
	for index,music in enumerate(getFilesNames(folder)):
		try:
			fileExtension = (re.search('\.(\w+)\Z',music, re.I).group(1)).lower()
		except:
			mlog.log.debug( 'Not possible to get the file extension')
		else:
			try:
				fileClass = audiofileDict[fileExtension]
			except Exception as error:
				mlog.log.debug('File '+music+' has a not recognized extension.')
			else:
				try:
					exec('''audio = '''+fileClass+'''("'''+music+'''")''')
				except ID3NoHeaderError:
					mlog.log.debug('File '+' has no ID3 tag. Trying to add it.')
					audio = ID3()
					audio.add(TPE1(encoding=3, text=u'Artist'))
					audio.save(music)
					exec('''audio = '''+fileClass+'''("'''+music+'''")''')
				except Exception as error:
					mlog.log.error( 'Error setting tag '+tag+' of file '+music+': '+str(error))
				finally:
					try:
						audio[tag] = tagInfo
						mlog.log.info( 'Setting tag '+tag+' of file '+music)
						audio.save()
					except Exception as error:
						mlog.log.error( 'Error setting tag '+tag+' of file '+music+': '+str(error))

