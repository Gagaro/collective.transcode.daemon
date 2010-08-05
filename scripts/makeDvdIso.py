#!./bin/daemonpy

import sys, subprocess, datetime, tempfile, os
import feedparser

if len(sys.argv) == 3:
    input_rss = sys.argv[1]
    output_iso = sys.argv[2]

else:
    print 'too many or too few arguments in makeDvdIso command'
    sys.exit(1)

try:
    rss = feedparser.parse(input_rss)
except:
    print 'cannot open rss feed url'

cmd = [u'./bin/todisc', u'-menu-fontsize', u'36', u'-title-color', u'\'#ff7700\'', u'-stroke-color', u'black']

dvd_title = unicode(rss.feed.title)
cmd += [u'-menu-title'] 
cmd += [dvd_title]

files = []
titles = []

tempdir = tempfile.mkdtemp()

for entry in rss.entries:
    titles.append(entry.title)

for video in os.listdir(tempdir):
    #TODO 1: download file on temp dir 
    files.append(tempdir+video)


cmd += [u'-files'] + files
cmd += [u'-titles'] + titles
cmd += [u'-out']
cmd += [unicode(output_iso)]

try:
    subprocess.call(cmd)
except:
    print 'problem when calling tovid command'


try:
    subprocess.call("mkisofs -o %s %s" % (output_iso, tempdir))
except:
    print 'problem when calling mkisofs command' % 

    
#TODO 2: send callback that dvd is ready
#TODO 3: delete dvd and folder after 

