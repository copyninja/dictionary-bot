#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Dictionary
# Copyright 2010 Santhosh Thottingal <santhosh.thottingal@gmail.com>
# http://www.smc.org.in
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# If you find any bugs or have any suggestions email: santhosh.thottingal@gmail.com
# URL: http://www.smc.org.in


import re
import urllib
import urllib2
import os,sys
from BeautifulSoup import BeautifulSoup
def get_def(word, src_lang,dest_lang):
    quotedfilename = urllib.quote(word.encode('utf-8')) 
    link = "http://"+dest_lang+".wiktionary.org/w/api.php?action=parse&format=xml&prop=text|revid|displaytitle&callback=?&page="+quotedfilename
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    soup=None
    try:
        soup = BeautifulSoup(opener.open(link).read())
    except:
		return None    
    text=  BeautifulSoup(bs_preprocess(soup('text')[0].string))
    meanings = None
    for li in text('li'):
		try:
		    if meanings==None:
			    meanings =""
		    if li.a:
		        meanings+=li.a.string+"\n"
		    else:    
		        meanings+=li.string+"\n"
		except:
			pass        
    return meanings
def bs_preprocess(html):
    html = html.replace("&lt;","<")
    html = html.replace("&gt;",">")
    html = html.replace('&quot;','\'')
    return html 
if __name__ == '__main__':
    print get_def(u'ഉര്‍വീധരന്‍','ml','ml')
    print get_def('Mars','ml','ml')
    print get_def('help','ml','ml')
    print get_def('father','ml','ml')
    print get_def('fathehghghghr','ml','ml')
