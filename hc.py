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


class cluster:

    def __init__(self, pnts, d):
        self.level = 0
        self.name = ""
        self.points = pnts
        self.center = list()
        for i in range(0, d):
            self.center.append(0.0)
        self.num_points = 0

    def get_points(self):
        pt = list()
        for i in range(0, len(self.points)):
            if "list" in str(type(self.points[i])):
                pt.append(self.points[i][:])
            else:
                pt = pt + self.points[i].get_points()

        return pt

    def set_center(self):
        pt = self.get_points()
        for i in range(0, len(self.center)):
            self.center[i] = 0.0

        for p in pt:
            for i in range(0, len(self.center)):
                self.center[i] = self.center[i] + p[i]

        for i in range(0, len(self.center)):
            self.center[i] = self.center[i] / len(pt)


class process:

    def __init__(self, points, d):

        self.clusters = list()
        self.dimansions = d
        for p in points:
            c = cluster([p[1]], d)
            c.name = p[0]
            c.level = 0
            c.set_center()
            self.clusters.append(c)

    def distence(self, p1, p2):
        sm = 0.0
        for i in range(0, len(p1)):
            sm = sm + (p1[i] - p2[i]) ** 2.0

        return sm ** 0.5

    def find_nearest(self):
        mn = 10000000
        p = (-1, -1)
        for i in range(0, len(self.clusters) - 1):
            for j in range(i + 1, len(self.clusters)):
                d = self.distence(self.clusters[i].center,
                                    self.clusters[j].center)
                if d < mn:
                    mn = d
                    p = (i, j)

        return p

    def marge(self, i, j, l):
        c = cluster([self.clusters[i], self.clusters[j]], self.dimansions)
        c.level = l
        c.set_center()
        return c

    def run(self):
        level = 1
        while len(self.clusters) > 2:
            print "level : ", level
            i, j = self.find_nearest()
            mc = self.marge(i, j, level)
            clusters_tmp = list()
            for k in range(0, len(self.clusters)):
                if k == i or k == j:
                    continue
                c = cluster([self.clusters[k]], self.dimansions)
                c.level = level
                c.set_center()
                clusters_tmp.append(c)
            clusters_tmp.append(mc)
            self.clusters = clusters_tmp
            level = level + 1


class preprocesser:

    def __init__(self):
        self.endings = {}
        self.stop = list()
        #self.words = {}
        self.sym = ['.', ',', '\'', '"', ';', ':', '-', '_',
                    '?', '(', ')', '[', ']', '/', '\\', '!',
                    '0', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', '*', '\n', '\t']

        self.process_endings()
        self.process_stop()

    def stm(self, word):
        l = len(word)
        if l > 11:
            counter = 11
        else:
            counter = l - 1
        for i in range(0, counter):
            end = word[l - counter + i:]
            if self.endings[counter - i].get(end, 0) == 1:
                word = word[:l - counter + i]
                return word
            elif len(end) > 2 and end[0] == end[1]:
                end = end[2:]
                if self.endings[counter - i].get(end, 0) == 1:
                    word = word[:l - counter + i + 1]
                    return word
        return word

    def process_endings(self):

        try:
            f = open("endings", 'r')
        except IOError:
            print "ERROR : ' endings ' is missing"
            exit(0)
        en = f.read().splitlines()
        for i in range(1, 12):
            self.endings[i] = {}

        for e in en:
            es = e.split()
            if es[1] == '1':
                self.endings[len(es[0])][es[0]] = 1
            elif es[1] == '2':
                self.endings[len(es[0]) + 2][es[0]] = 1

    def process_stop(self):
        try:
            f = open("stop", 'r')
        except IOError:
            print "ERROR : ' stop ' is missing"
        lines = f.read().splitlines()
        for line in lines:
            self.stop.append(line)  # [line] = 1

    def remove_sym(self, word):
        for c in self.sym:
            word = word.replace(c, '')
        return word

    def process(self, words_list):
        words = {}
        count = 0
        for word in words_list:
            word = word.lower()
            word = self.remove_sym(word)
            if len(word) <= 1:
                continue
            if word in self.stop:
                continue
            count = count + 1
            word = self.stm(word)
            if words.get(word, 0) == 0:
                words[word] = 1.0
            else:
                words[word] = words[word] + 1.0
        for w in words.keys():
            words[w] = words[w] / count
        return words
