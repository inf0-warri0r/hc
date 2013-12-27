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


class level_page:

    def __init__(self, lvl, art, h, f):
        self.level = lvl
        self.header = h
        self.footer = f
        self.articles = art

    def write(self, cluster, art, f):
        f.write("<br/> <h3> Cluster : " + cluster + "</h3><br/>")

        f.write("<ul>")
        for a in art:
            f.write("<li>" + a + "</li>")
        f.write("</ul>")

    def write_page(self):
        f = ""
        try:
            f = open("pages/" + str(self.level) + ".html", 'w')
        except IOError:
            print "ERROR : ' file ' is missing"

        f.write(self.header)
        f.write("<h2> Level : " + str(self.level) + "</h2>")

        keys = sorted(self.articles.keys())
        for key in keys:
            self.write(key, self.articles[key], f)
        f.write(self.footer)
