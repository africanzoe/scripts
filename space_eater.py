#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import argparse
import shutil



def space_eater(path, show=False):
    if show:
        try:
            for f in os.scandir(path):
                if ' ' in f.name:
                    print(" [ {} ] {:<} -> {:<}".format('d' if f.is_dir() else 'f', path+f.name, path+f.name.replace(" ", "_")))
                elif f.is_dir():
                    space_eater(path+'/'+f.name, True)
        except:
            pass
    else:
        for f in os.scandir(path):
            shutil.move(path+'/'+f.name, path+'/'+f.name.replace(" ", "_"))
            if f.is_dir():
                space_eater(path+'/'+f.name)

def parse_args():
    parser = argparse.ArgumentParser(description='Filename space eater')
    parser.add_argument("path",
                        nargs='?',
                        metavar='dir',
                        default=os.getcwd(),
                        help="target directory, defaults to cwd")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a",
                        "--apply",
                        action="store_true",
                        help="convert the spaces to underscores for all files under the dir")

    group.add_argument("-s",
                        "--show",
                        action="store_true",
                        help="show changes without applying them")

    return parser.parse_args()

def main():
    args = parse_args()

    if args.apply:
        if os.path.exists(args.path) and os.path.isdir(args.path):
            space_eater(args.path)
        else:
            print("The path you entered either doesn't exist or is not a directory")

    if args.show:
        print('The list of file(s)/dir(s) to rename under the path "'+args.path+'":')
        space_eater(args.path, show=True)

if __name__ == '__main__':
    main()
