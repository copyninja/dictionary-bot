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
import sqlite3


INSERT_STATMT = "INSERT INTO %s (word, meaning) values ('%s','%s')"
SELECT_STATMT = "SELECT word, meaning from %s  where word='%s'"

INSERT_UNDEFINED = "INSERT INTO undefined_words (word,frequency) values ('%s',%d)"
UPDATE_UNDEFINED = "UPDATE undefined_words set frequency = frequency + 1 where word = '%s'"
SELECT_UNDEFINED = "SELECT count(*) from undefined_words where word = '%s'"

# def logger(message):
#     fp = os.open('wiktionary.log',os.O_RDWR)
#     os.write(fp,message)
#     os.close(fp)

def get_def(word, src_lang,dest_lang):
    meaning_from_db = None
    # logger(word)
    try:
        meaning_from_db = get_meaning_from_database(word,src_lang)
    except:
        pass    
    if meaning_from_db != None:
        return meaning_from_db[1]
    quotedfilename = urllib.quote(word.encode('utf-8')) 
    link = "http://"+dest_lang.split('_')[0]+".wiktionary.org/w/api.php?action=parse&format=xml&prop=text|revid|displaytitle&callback=?&page="+quotedfilename
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    soup=None
    meanings = None
    try:
        soup = BeautifulSoup(opener.open(link).read())
        text=  BeautifulSoup(bs_preprocess(soup('text')[0].string))

        for li in text('li'):
            try:
                if meanings==None:
                    meanings =""

                a = li('a')

                if isinstance(a,list):
                    for link in a:
                        meanings += link.string+", "
                elif li.a:
                    meanings+=li.a.string+", "
                else:    
                    meanings+=li.string+", "

            except:
                pass   
        if meanings!= None:
            if src_lang == "ml_IN":
                meanings = normalize_ml(meanings)
            meanings = meanings.rstrip(', ')
            add_to_database(word, meanings,src_lang)
            return meanings
    except:
        pass
    
    add_undefined(word)
    return None

def bs_preprocess(html):
    html = html.replace("&lt;","<")
    html = html.replace("&gt;",">")
    html = html.replace('&quot;','\'')
    return html 
    
def add_to_database(word, meaning,src_lang):
    global INSERT_STATMT
    conn = sqlite3.connect('/home/vasudev/kannada-dictionary-bot/wiktionary.sqlite')
    c = conn.cursor()

    insert = None
    if src_lang == "ml_IN":
        insert = INSERT_STATMT % ("mlwiktionary",word,meaning)
    elif src_lang == "kn_IN":
        insert = INSERT_STATMT % ("knwiktionary",word,meaning)
    c.execute(insert)
    conn.commit()
    c.close()
    conn.close()

def add_undefined(word):
    global INSERT_UNDEFINED,SELECT_UNDEFINED,UPDATE_UNDEFINED
    conn = sqlite3.connect('/home/vasudev/kannada-dictionary-bot/wiktionary.sqlite')
    c = conn.cursor()

    c.execute(SELECT_UNDEFINED % (word))
    count = c.fetchone()
    if count[0] == 0:
        c.execute(INSERT_UNDEFINED % (word,1))
    else:
        c.execute(UPDATE_UNDEFINED % (word))

    conn.commit()
    c.close()
    conn.close()
    
    


def get_meaning_from_database(word,src_lang):
    global SELECT_STATMT

    conn = sqlite3.connect('/home/vasudev/kannada-dictionary-bot/wiktionary.sqlite')
    if src_lang == "ml_IN":
        select = SELECT_STATMT % ("mlwiktionary",word)
    elif src_lang == "kn_IN":
        select = SELECT_STATMT % ("knwiktionary",word)
    c = conn.cursor()
    rows = c.execute(select)
    result = None
    for row in rows:
        result = row
    conn.commit()
    c.close()
    return result 
    
def normalize_ml (text):
    text = text.replace(u"ൺ" , u"ണ്‍")
    text = text.replace(u"ൻ", u"ന്‍")
    text = text.replace(u"ർ", u"ര്‍")
    text = text.replace(u"ൽ", u"ല്‍")
    text = text.replace(u"ൾ", u"ള്‍")
    text = text.replace(u"ൿ", u"ക്‍")
    text = text.replace(u"ന്‍റ", u"ന്റ")
    return text   
    
if __name__ == '__main__':
    #add_to_database("hi","hello")
    #get_meaning_from_database("hi")
    #print get_def(u'ഉര്‍വീധരന്‍','ml_IN','ml_IN').encode("utf-8")
    #print get_def('Mars','ml_IN','ml_IN').decode("utf-8")
    #print get_def('help','ml','ml')
    #print get_def('father','ml','ml')
    #print get_def('fathehghghghr','ml','ml')
    #print get_def('fat','ml','ml')
    print get_def('aaaa','kn_IN','kn_IN').encode('utf-8')
