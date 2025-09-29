#!/usr/bin/env python3
import argparse
import os
import shutil
import sys

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', required=True, help='PyInstaller dist folder')
    parser.add_argument('--out', required=True, help='Installer staging folder')
    parser.add_argument('--appname', required=True)
    parser.add_argument('--main-exe', required=True)
    args = parser.parse_args()

    dist = args.dist
    out = args.out
    name = args.appname
    main_exe = args.main_exe

    if not os.path.exists(dist):
        print("Dist folder not found:", dist)
        return 2
    ensure_dir(out)

    # copy exe
    exe_src = None
    # If user gave an explicit main exe path, prefer it
    if os.path.exists(main_exe):
        exe_src = main_exe
    else:
        # try common places
        candidate = os.path.join(dist, name + '.exe')
        if os.path.exists(candidate):
            exe_src = candidate
        else:
            # try scanning dist for exe
            for f in os.listdir(dist):
                if f.lower().endswith('.exe'):
                    exe_src = os.path.join(dist, f)
                    break

    if not exe_src:
        print("No executable found in dist. Please build first.")
        return 3

    shutil.copy2(exe_src, os.path.join(out, name + '.exe'))

    # copy README and LICENSE if exist in project root
    for fname in ('README.md','LICENSE.txt','app.ico'):
        if os.path.exists(fname):
            shutil.copy2(fname, out)

    print("Prepared installer folder:", out)
    return 0

if __name__ == '__main__':
    sys.exit(main())
