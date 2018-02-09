
from creategraph import create_from_constants
from passes import *

import random

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
    print(world)
    
main()
