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


class list_page:

    def __init__(self, lvls, hd, ft):
        self.levels = sorted(lvls)
        self.header = hd
        self.footer = ft

    def write_page(self):
        f = ""
        try:
            f = open("pages/list.html", 'w')
        except IOError:
            print "ERROR : ' list.html ' is missing"

        f.write(self.header)
        f.write("<h3>Levels : </h3>")
        f.write("<ul>")
        for l in self.levels:
            f.write("<li>")
            st = "<a href=\'index.html?l=" + str(l)
            st = st + ".html\' target=\'top\'> Level : "
            st = st + str(l) + "</a>"
            f.write(st)
            f.write("</li>")

        f.write(self.footer)
