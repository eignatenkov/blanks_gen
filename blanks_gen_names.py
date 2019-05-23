#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
import pdb
import sys
import os
import codecs
import subprocess
import shlex
import shutil
import argparse
try:
    unicode
except NameError:
    unicode = str


def make_filename(filename, i, maxi):
    basename = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    zf = len(unicode(maxi))
    return basename + '_{}'.format(unicode(i).zfill(zf)) + ext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('teams', type=int)
    parser.add_argument('--addteams')
    parser.add_argument('--blanks', default='blanks.tex')
    parser.add_argument('--placeholder', default='\hrulefill')
    parser.add_argument('--logs', action='store_true')
    parser.add_argument('--output_dir', default=None)
    args = parser.parse_args()

    blueprint = codecs.open(args.blanks, 'r', 'utf8').read()

    if args.output_dir:
        shutil.copy(args.blanks, args.output_dir)
        shutil.copy('blanksheader.tex', args.output_dir)
        os.chdir(args.output_dir)

    numbers = list(range(1, args.teams + 1))
    if args.addteams:
        numbers = numbers + [int(x) for x in args.addteams.split(',')]

    # team_names = [u'Алые Паруса', u'Берлитанты', u'Наш Вариант Лучше', u'Палладины', u'Понты Пилата', u'Псевдопептиды']
    team_names = [u'Алые Паруса', u'Ненадёжные']

    new_filenames = []
    for i in numbers:
        nf = make_filename(args.blanks, i, max(numbers))
        new_filenames.append(nf)
        print('processing {}'.format(nf))
        with codecs.open(nf, 'w', 'utf8') as f:
            f.write(blueprint.replace(
                args.placeholder, team_names[i-1] + '\\hfill'
            ))
        subprocess.call(
            shlex.split(
                'xelatex -synctex=1 -interaction=nonstopmode "{}"'.format(nf)),
            stdout=open(os.devnull, 'wb')
        )
    for x in new_filenames:
        os.remove(x)
    if not args.logs:
        for x in os.listdir(os.getcwd()):
            if x.endswith(('.log', '.aux', '.out', '.gz')):
                os.remove(x)


if __name__ == "__main__":
    main()
