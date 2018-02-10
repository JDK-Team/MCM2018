#!/usr/bin/env python3

from updates import *

import random

#logging
import argparse
import logging

# LOGGING SETUP

parser = argparse.ArgumentParser(description='Command-line arguments.')
parser.add_argument("-l", 
                    "--log", 
                    dest="logLevel", 
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                    help="Set the logging level")

args = parser.parse_args()
if args.logLevel:
    logging.basicConfig(level=getattr(logging, args.logLevel))

from creategraph import create_from_constants
# ways to run a pass

def run_pass_seq(world, passfunc):
    for i in range(0,len(world.regions)):
        passfunc(world,i)

def run_pass_stoc(world, passfunc):
    ord = list(range(0,len(world.regions)))
    random.shuffle(ord)
    for i in ord:
        passfunc(world, i)

# run an entire iteration of a model

def model1_compiler_pass(world):
    run_pass_seq(world, birth)
    run_pass_seq(world, death)
    run_pass_seq(world, migration)
    #run_pass_seq(world, regional)

def model1_stochastic_pass(world):
    def node_pass(world, n):
        birth(world, n)
        death(world, n)
        migration(world, n)
        #regional(world, n)
    run_pass_stoc(world, node_pass)

# run the whole model

def model1_compiler(world, nIter):
    for i in range(0,nIter):
        model1_compiler_pass(world)

def model1_stochastic(world, nIter):
    for i in range(0,nIter):
        model1_stochastic_pass(world)

def main():
    world = create_from_constants()
    
    model1_compiler(world, 1)
    logging.info(world)
    
main()
