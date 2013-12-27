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

import level_page
import list_page


class resultss:

    def __init__(self, p):
        self.pr = p
        self.read()

    def read(self):
        try:
            f = open("header.html", 'r')
        except IOError:
            print "ERROR : ' file ' is missing"

        self.header = f.read()

        try:
            f = open("footer.html", 'r')
        except IOError:
            print "ERROR : ' file ' is missing"

        self.footer = f.read()

    def get_names(self, cls):
        if cls.name != "":
            return [cls.name]
        else:
            lst = list()
            for c in cls.points:
                lst = lst + self.get_names(c)
            return lst

    def get_cls(self, cls):
        if cls.name != "":
            return []
        else:
            return cls.points

    def write_levels(self):
        lst = self.pr.clusters[:]

        level = self.pr.clusters[0].level
        lvls = list()
        while level > 0:
            lvls.append(level)
            lst_tmp = list()
            for ll in lst:
                lst_tmp = lst_tmp + ll.points[:]
            cls = {}
            for i in range(0, len(lst_tmp)):
                cls[str(i)] = self.get_names(lst_tmp[i])
            lp = level_page.level_page(level, cls, self.header, self.footer)
            lp.write_page()
            lst = lst_tmp
            level = lst[0].level

        list_page.list_page(lvls, self.header, self.footer).write_page()
