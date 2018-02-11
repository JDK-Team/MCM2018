#!/usr/bin/env python3

from updates import *
from data_retrival import *

import random
import numpy as np

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
    #logging.basicConfig(level=logging.DEBUG)

from creategraph import create_from_constants, create_graph
# ways to run a pass

def run_pass_seq(world, subs, passfunc):
    for i in range(0,len(world.regions)):
        passfunc(world, subs,i)

def run_pass_stoc(world, subs, passfunc):
    ord = list(range(0,len(world.regions)))
    random.shuffle(ord)
    for i in ord:
        passfunc(world, subs, i)

# run an entire iteration of a model

def model1_compiler_pass(world, subs):
    run_pass_seq(world, subs, birth)
    #logging.debug(world, subs.regions[4])
    run_pass_seq(world, subs, death)
    #logging.debug(world.regions[4])
    run_pass_seq(world, subs, migration)
    #run_pass_seq(world, subs, regional)

def model1_stochastic_pass(world, subs):
    def node_pass(world, subs, n):
        birth(world, subs, n)
        death(world, subs, n)
        migration(world, subs, n)
        #regional(world, subs, n)
    run_pass_stoc(world, subs, node_pass)

def model1_bd_comppass(world, subs):
    run_pass_seq(world, subs, birth)
    run_pass_seq(world, subs, death)

def model1_bd_comp_extradeath(world, subs):
    run_pass_seq(world, subs, birth)
    run_pass_seq(world, subs, death)
    run_pass_seq(world, subs, death)

def model1_stoch_bd(world, subs):
    run_pass_stoc(world, subs, birth)
    run_pass_stoc(world, subs, death)

def model1_stoch_full_bd(world, subs):
    def bd_upd(world, subs, n):
        birth(world, subs, n)
        death(world, subs, n)
    run_pass_stoc(world, subs, bd_upd)

def model1_5_5yearpass(world, subs, startyear):
    for i in range(0,5*subs):
        model1_compiler_pass(world, subs)
    run_pass_seq(world, subs, lambda world,subs,n: update_birth(world, startyear+5, n))
    run_pass_seq(world, subs, lambda world,subs,n: update_death(world, startyear+5, n))


# run the whole model

def measuringStick():
    names = identifiers()
    language_names = lang_names('L1_Language_Data.csv')
    pops = scalar_data('regionPops.csv', 2010)
    brates = scalar_data('r_birthRate.csv', 2010)
    drates = scalar_data('r_deathRate.csv', 2010)
    k_vals = mig_data('actual_r_migration2010_withk.csv')
    #logging.debug('K VALUES')
    #print(k_vals)
    #for i in range(0,len(k_vals)):
        #logging.debug(k_vals[i,:])
    L1s = lang_data('L1_Language_Data.csv')
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    popRegionalErrorData = []
    popTotalErrorData = []
    numDivisions = 1
    for i in range(0,5*numDivisions):
        model1_bd_comppass(world, numDivisions)
    
    return pop2015 - populations(world)

def model1_test():
    names = identifiers()
    language_names = lang_names('L1_Language_Data.csv')
    pops = scalar_data('regionPops.csv', 2010)
    brates = scalar_data('r_birthRate.csv', 2010)
    drates = scalar_data('r_deathRate.csv', 2010)
    k_vals = mig_data('actual_r_migration2000_withk.csv')
    #logging.debug('K VALUES')
    #print(k_vals)
    #for i in range(0,len(k_vals)):
        #logging.debug(k_vals[i,:])
    L1s = lang_data('L1_Language_Data.csv')
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    popRegionalErrorData = []
    popTotalErrorData = []
    numDivisions = 12
    for i in range(0,40*numDivisions):
        model1_compiler_pass(world, numDivisions)
        year = i/numDivisions + 1
        if(year%5 == 0): #every 5 years
            projectedPops = scalar_data('projectedPopData.csv', 2010+int(year))
            #print(projectedPops)
            popRegionalErrorData.append((populations(world) - projectedPops*1000)/(projectedPops*1000))
            popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))

        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    print(popRegionalErrorData)
    print(popTotalErrorData)
    pop2015 = scalar_data('regionPops.csv', 2015)

    #logging.info(np.sum(pop2015))
    #logging.info(np.sum(populations(world)))
    #logging.info(populations(world))

    #logging.info(pop2015 - populations(world))
    #logging.debug([usa for usa in world.regions if usa.name == 'USA'])

def writecsv():
    return 0

def model1_5_percenterror():
    names = identifiers()
    language_names = lang_names('L1_Language_Data.csv')
    pops = scalar_data('regionPops.csv', 2010)
    brates = scalar_data('r_birthRate.csv', 2010)
    drates = scalar_data('r_deathRate.csv', 2010)
    k_vals = mig_data('actual_r_migration2000_withk.csv')
    #logging.debug('K VALUES')
    #print(k_vals)
    #for i in range(0,len(k_vals)):
        #logging.debug(k_vals[i,:])
    L1s = lang_data('L1_Language_Data.csv')
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    popRegionalErrorData = []
    popTotalErrorData = []
    numDivisions = 1
    num5yearChuncks = 8
    for i in range(0,num5yearChuncks):
        model1_5_5yearpass(world, numDivisions, 2010)
        projectedPops = scalar_data('projectedPopData.csv', 2010+5*i)
        #print(projectedPops)
        popRegionalErrorData.append(((populations(world) - projectedPops*1000)/(projectedPops*1000)))
        popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))

        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    print(popRegionalErrorData)
    print(popTotalErrorData)
    popRegionalErrorData = np.transpose(np.asarray(popRegionalErrorData))
    #np.savetxt("popRegionalError_12.csv", popRegionalErrorData, delimiter=",")
    np.savetxt("L1_1_2050.csv", L1s, delimiter=",")

    #pop2015 = scalar_data('regionPops.csv', 2015)

    #logging.info(np.sum(pop2015))
    #logging.info(np.sum(populations(world)))
    #logging.info(populations(world))

    #logging.info(pop2015 - populations(world))
    #logging.debug([usa for usa in world.regions if usa.name == 'USA'])
# get statistics
def populations(world):
    return np.array([reg.population for reg in world.regions])

def main():
    #world = create_from_constants()
    
    #model1_compiler(world, subs, 1)
    #logging.info(world)
    #model1_test()
    model1_5_percenterror()

main()
