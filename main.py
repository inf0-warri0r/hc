#! /usr/bin/env python

"""
Author : tharindra galahena (inf0_warri0r)
Project: clustering wikipedia articles using hierarchical clustering
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 26/12/2013
License:

     Copyright 2013 Tharindra Galahena

This is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
this. If not, see http://www.gnu.org/licenses/.

"""

import hc
import results
import re
from json import *
import json


def remove_dimensions(w_dic):
    shortest = w_dic.keys()[0]
    for key in w_dic:
        if len(w_dic[key]) < len(w_dic[shortest]):
            shortest = key

    print len(w_dic[shortest])
    for s in w_dic[shortest].keys():
        remove = True
        number = w_dic[shortest][s]
        for key in w_dic.keys():
            if w_dic[key].get(s, 0) - number > 0.01:
                remove = False
                continue
            elif w_dic[key].get(s, 0) - number < - 0.01:
                remove = False
                continue

        if remove:
            for key in w_dic.keys():
                if w_dic[key].get(s, 0) != 0:
                    del w_dic[key][s]

    return w_dic


print ""
print "--------------------------------------------------------------------"
print " -- CLUSTERING WIKIPEDIA ARTICLES USING HIERARCHICAL CLUSTERING  -- "
print "                                                                    "
print "   Author : tharindra galahena (inf0_warri0r)                       "
print "   Blog   : http://www.inf0warri0r.blogspot.com                     "
print "--------------------------------------------------------------------"
print "\n"

p = hc.preprocesser()

num_of_articles = 100
articles = {}
count = 0
title = ""
lst = list()

print "You can read the articles and preprocess from the bigining"
print "or read already processed data from 'word_list' file. Type"
print "'y' to read articles or 'n' to read 'word_list'.\n"

rd = raw_input("Read the articles and preprocess [y/n] :")

if rd[0] == 'y' or rd[0] == 'Y':

    while 1:
        name = raw_input("Enter the data set file path : ")
        print "\nReading articles...\n"

        try:
            f = open(name, 'r')
            break
        except IOError:
            print "ERROR : \'" + name + "\' doesn\'t exists"

    lines = f.read().splitlines()

    for l in lines:
        words = re.split(r'\t+', l)
        if words[0] != title:
            print count + 1, " - ", title

            if len(lst) > 0:
                articles[title] = p.process(lst)
            lst = list()
            title = words[0]
            count = count + 1
            if count > num_of_articles - 1:
                break
        if int(words[1]) < 4:
            lst = lst + words[2].split()

    articles = remove_dimensions(articles)
    s = JSONEncoder().encode(articles)

    f = open('word_list', 'w')
    f.write(str(s))
    f.close()

    print "Done...\n"

else:

    print "\nLoading word_list file ...\n"

    try:
        f = open("word_list", 'r')
    except IOError:
        print "ERROR : 'word_list' is missing"
        exit(0)

    articles = json.loads(f.read())

    print "Done ...\n"

ww = {}
for key in articles.keys():
    ww.update(articles[key].copy())

words = list()

try:
    f = open("selected", 'r')
except IOError:
    print "ERROR : 'selected' is missing"
    exit(0)

words = f.read().splitlines()

for key in ww.keys():
    if key not in words:
        for key2 in articles.keys():
            if articles[key2].get(key, 0) != 0:
                del articles[key2][key]

ww = {}
for key in articles.keys():
    ww.update(articles[key].copy())

points = list()
for key in articles.keys():
    tmp = list()
    tmp.append(key)
    p = list()
    for key2 in ww.keys():
        p.append(articles[key].get(key2, 0.0))
    tmp.append(p)
    points.append(tmp)

print "Start Clustering ...\n"

pr = hc.process(points, len(ww))
pr.run()

print "\nDone...\n"

print "Creating Output documents...\n"

res = results.resultss(pr)
res.write_levels()

print "Done ...\n"
