#!/usr/bin/env python

from __future__ import division, print_function
import os
import click

if 'TREETOOL_BASEPATH' in os.environ:
    os.chdir(os.environ['TREETOOL_BASEPATH'])

@click.group()
def cli():
    pass

@cli.command()
@click.option('--states_to_skip', type=int, default=120000)
@click.argument('input_file', type=click.File())
@click.argument('output_file', type=click.File('w'))
def clean_tree(input_file, output_file, states_to_skip):
    state = 0
    skip = True
    for line in input_file:
        if skip and not line.startswith('tree '):
            output_file.write(line)
        if line.startswith('tree '):
            skip = False
        if not skip:
            while '\0' in line and line != '':
                # corruption, skip this but keep its state number
                line = input_file.readline()
            fields = line.split()
            output_file.write(' '.join(['tree', 'STATE_' + str(state)] + fields[2:]))
            state = state + states_to_skip
    output_file.close()

@cli.command()
@click.option('--states_to_skip', type=int, default=12000)
@click.argument('input_file', type=click.File())
def check_tree(input_file, states_to_skip):
    old_state = state = 0
    messed_up = False
    skip = True
    for line in input_file:
        if line.startswith('tree '):
            skip = False
        if not skip:
            if '\0' in line:
                print("null true")
            fields = line.split()
            state_str = fields[1]
            state = int(state_str[6:])
            state_diff = state - old_state
            if state != 0 and state_diff != states_to_skip:
                messed_up = True
                print("skip before:", state, old_state, state_diff, len(fields), state_diff / states_to_skip, '\0' in line)
            old_state = state
    if not messed_up:
        print("tree is ok")
    else:
        print("tree is NOT OK")

if __name__ == '__main__':
    cli()
