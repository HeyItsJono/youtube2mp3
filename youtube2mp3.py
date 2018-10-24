import os
import subprocess

cd = False
while cd == False:
	dir = raw_input("No quotes, even if there are spaces. Full path to dir containing file(s): ")
	try:
		os.chdir(dir)
	except OSError:
		print "Cannot cd to directory.\n"
		continue
	cd = True
	
trim_global = raw_input("Trimming any audio? (y/n, n is default) ")
if trim_global == 'y':
	trim_global = True
else:
	trim_global = False

print "\nWorking directory: {0}\nNumber of files in working directory: {1}\n".format(os.getcwd(),len(os.listdir(os.getcwd())))

if not os.path.exists(os.getcwd() + "/mp3"): os.mkdir(os.getcwd() + "/mp3")

if trim_global:
	trim_list = []
	print "May ask you to trim non-music files - just leave blank and press enter, won't have any effect."
	for item in os.listdir(os.getcwd()):
		print "============================\n"
		print "Trimming {0}".format(item)
		print "Leave blank if you want to use default start/end time(s)."
		trim_list.append({'name':item, 'start':raw_input('Start audio at (HH:MM:SS.msec): '), 'end':raw_input('End audio at (HH:MM:SS.msec): ')})
		print '\n'
	for item in trim_list:
		if item['start'] == '': item['start'] = "00:00:00.0"
		if item['end'] != '':
			print "Attempting to convert {0} to mp3, starting at {1} and trimming end to {2}...\n".format(item['name'], item['start'], item['end'])
			print subprocess.call('''ffmpeg -i "{0}" -q:a 0 -ss {1} -to {2} "{3}/mp3/{4}mp3"'''.format(item['name'],item['start'],item['end'],os.getcwd(),item['name'][:-3]))
		else:
			print "Attempting to convert {0} to mp3, starting at {1} and no trimming off the end...\n".format(item['name'], item['start'])
			print subprocess.call('''ffmpeg -i "{0}" -q:a 0 -ss {1} "{2}/mp3/{3}mp3"'''.format(item['name'],item['start'],os.getcwd(),item['name'][:-3]))
else:
	print "============================\n"
	for item in os.listdir(os.getcwd()):
		print "Attempting to convert {0} to mp3, no trimming...\n".format(item)
		print subprocess.call('''ffmpeg -i "{0}" -q:a 0 "{1}/mp3/{2}mp3"'''.format(item,os.getcwd(),item[:-3]))

print "\n==============================\nDone!"