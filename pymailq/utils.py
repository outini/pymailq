#
#    Postfix queue control python tool (pymailq)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of pymailq
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

from functools import wraps
from collections import Counter


def sorter(function):
    """Result sorter decorator.

    This decorator inspect decorated function arguments and search for
    known keyword to sort decorated function result.


    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        args = list(args)  # conversion need for arguments cleaning
        sortkey = "date"  # default sort by date
        reverse = True  # default sorting is desc
        if "sortby" in args:
            sortby_idx = args.index('sortby')
            args.pop(sortby_idx)  # pop option, next arg is value

            try:
                sortkey = args.pop(sortby_idx)
            except IndexError:
                raise SyntaxError("sortby requires a field")

            if "asc" in args:
                args.pop(args.index('asc'))
                reverse=False
            elif "desc" in args:
                args.pop(args.index('desc'))

        elements = function(*args, **kwargs)

        try:
            sorted_elements = sorted(elements,
                                     key=lambda x: getattr(x, sortkey),
                                     reverse=reverse)
        except AttributeError:
            msg = "elements cannot be sorted by %s" % (sortkey)
            raise SyntaxError(msg)

        return sorted_elements
    wrapper.__doc__ = function.__doc__
    return wrapper

def ranker(function):
    """Result ranker decorator
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        args = list(args)  # conversion need for arguments cleaning
        rankkey = None
        if "rankby" in args:
            rankby_idx = args.index('rankby')
            args.pop(rankby_idx)  # pop option, next arg is value

            try:
                rankkey = args.pop(rankby_idx)
            except IndexError:
                raise SyntaxError("rankby requires a field")

        elements = function(*args, **kwargs)

        if rankkey is not None:
            try:
                rank = Counter()
                for element in elements:
                    rank[getattr(element, rankkey)] += 1

                # XXX: headers are taken in elements display limit :(
                ranked_elements = ['%-40s  count' % (rankkey), '='*48]
                for entry in rank.most_common():
                    key, value = entry
                    ranked_elements.append('%-40s  %s' % (key, value))
                return ranked_elements

            except AttributeError:
                msg = "elements cannot be ranked by %s" %(rankkey)
                raise SyntaxError(msg)

        return elements
    wrapper.__doc__ = function.__doc__
    return wrapper
