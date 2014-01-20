# -*- coding: utf-8 -*-
"""
    diff
    ~~~~

    This diff utility shall compare contents of file1 and file2, write to
    standard output a list of changes necessary to convert file1 into file2.

    :copyright: (c) 2014 by fsp.
    :license: BSD.
"""
import sys, os, time
import difflib
import optparse


def main():
    # OptionParser
    usage = "usage: python diff.py [options] fromfile tofile"
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", action="store_true", default=False, 
                      help="produce a context format diff (default)")
    parser.add_option("-u", action="store_true", default=False, 
                      help="produce a unified format diff")
    parser.add_option("-m", action="store_true", default=False, 
                      help="produce HTML side by side diff")
    parser.add_option("-n", action="store_true", default=False, 
                      help="produce a ndiff format diff")
    parser.add_option("-l", type="int", default=3, 
                      help="set number of context lines (default 3)")
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

    n = options.lines
    fromfile, tofile = args
    fromdate = time.ctime(os.stat(fromfile).st_mtime)
    todate = time.ctime(os.stat(tofile).st_mtime)
    fromlines = open(fromfile, 'U').readlines()
    tolines = open(tofile, 'U').readlines()

    if options.u:
        diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=n)
    elif options.n:
        diff = difflib.ndiff(fromlines, tolines)
    elif options.m:
        diff = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile,
                                            tofile, context=options.c,
                                            numlines=n)
    else:
        diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=n)

    sys.stdout.writelines(diff)


if __name__ == "__main__":
    main()
