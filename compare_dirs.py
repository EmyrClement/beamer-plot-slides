#!/usr/bin/env python

"""
This script takes a list of plot names, and list of dirs, and compares each plot amongst all dirs.

Usage:

    ./compare_dirs.py myPlots.pdf --dir "thisDir" --dir "anotherDir" --plotname "met.pdf" --plotname "jet_pt.pdf"
"""


import os
import argparse
import make_slides as ms
import json
import logging


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


def create_json_contents(args):
    """Create the JSON dict to be passed to make_slides.py"""
    json_dict = {
        'frontpage': {
            "title": args.title.replace("_", "\_"),
            "subtitle": "",
            "author": ""
        },
        'slides': []
    }

    for plot in args.plotname:
        this_dict = {"title": plot.replace("_", "\_")}
        plot_entries = [[os.path.join(this_dir, plot), this_label] for this_dir, this_label in zip(args.dir, args.dirlabel)]
        this_dict['plots'] = plot_entries
        json_dict['slides'].append(this_dict)
    
    return json_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="Output PDF filename")
    parser.add_argument("--dir", help="Directory to get plot from. Can be used multiple times", action="append")
    parser.add_argument("--dirlabel", help="Label to be given for dir. Must be used in conjunction with --dir, once per entry.", action="append")
    parser.add_argument("--plotname", help="Filename of plot. Can be used multiple times", action="append")
    parser.add_argument("--title", help="Title of presentation", default="Plot comparison")
    parser.add_argument("--template", help="Template beamer tex file", default="beamer_template.tex")
    parser.add_argument("--noCompile", help="Don't compile PDF", action='store_true')
    parser.add_argument("--noCleanup", help="Don't remove auxiliary aux/toc/log etc", action='store_true')
    parser.add_argument("-v", "--verbose", help="Run in verbose mode", action='store_true')
    parser.add_argument("--open", help="Open PDF", action='store_true')
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    # create a JSON config
    json_dict = create_json_contents(args)

    temp_json = os.path.splitext(args.output)[0] + ".json"
    with open(temp_json, "w") as f:
        f.write(json.dumps(json_dict, indent=4))
    
    # This is horrible FIXME
    new_args = [temp_json]
    new_args.append('--template=' + args.template)
    for name in ['noCompile', 'noCleanup', 'open']:
        if vars(args)[name]:
            new_args.append("--"+name)

    # run the main program as usual
    ms.main(new_args)

    # cleanup JSON
    os.remove(temp_json)
