#!/usr/bin/env python3

from updates import *
from data_retrival import *

import random
import numpy as np
import csv

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

def model2_compiler_bdm(world, subs):
    run_pass_seq(world, subs, birth_infl)
    run_pass_seq(world, subs, death)
    run_pass_seq(world, subs, migration_infl)

def model2_compiler_bmd(world, subs):
    run_pass_seq(world, subs, birth_infl)
    run_pass_seq(world, subs, migration_infl)
    run_pass_seq(world, subs, death)

def model2_compiler_dbm(world, subs):
    run_pass_seq(world, subs, death)
    run_pass_seq(world, subs, birth_infl)
    run_pass_seq(world, subs, migration_infl)

def model2_compiler_dmb(world, subs):
    run_pass_seq(world, subs, death)
    run_pass_seq(world, subs, migration_infl)
    run_pass_seq(world, subs, birth_infl)

def model2_compiler_mbd(world, subs):
    run_pass_seq(world, subs, migration_infl)
    run_pass_seq(world, subs, birth_infl)
    run_pass_seq(world, subs, death)

def model2_compiler_mdb(world, subs):
    run_pass_seq(world, subs, migration_infl)
    run_pass_seq(world, subs, death)
    run_pass_seq(world, subs, birth_infl)

def model1_stochastic_pass(world, subs):
    def node_pass(world, subs, n):
        birth(world, subs, n)
        death(world, subs, n)
        #migration(world, subs, n)
        #regional(world, subs, n)
    run_pass_stoc(world, subs, node_pass)

def model1_bd_comppass(world, subs):
    run_pass_seq(world, subs, birth)
    run_pass_seq(world, subs, death)

def model1_bd_combined_comppass(world, subs):
    run_pass_seq(world, subs, birth_and_death)

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
        logging.debug("YEARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR " + str(i))
        model1_bd_comppass(world, subs)
        #model1_stochastic_pass(world, subs)
    run_pass_seq(world, subs, lambda world,subs,n: update_birth(world, startyear+5, n))
    run_pass_seq(world, subs, lambda world,subs,n: update_death(world, startyear+5, n))

def model1_5_5yearpass_fine(world, subs, startyear):
    for i in range(0,5):
        for j in range(0,subs):
            model1_bd_comppass(world, subs)
        run_pass_seq(world, subs, lambda world,subs,n: update_birth_fine(world, startyear+i+1, n))
        run_pass_seq(world, subs, lambda world,subs,n: update_death_fine(world, startyear+i+1, n))

def model2_5yearpass(world, subs, startyear):
    for i in range(0,5*subs):
        logging.debug("YEAR " + str(i))
        model2_compiler_bmd(world, subs)
    run_pass_seq(world, subs, lambda world,subs,n: update_birth(world, startyear+5, n))
    run_pass_seq(world, subs, lambda world,subs,n: update_death(world, startyear+5, n))

def model2_5yearpass_fine(world, subs, startyear,i):
    for i in range(0,5):
        for j in range(0,subs):
            model2_compiler_bdm(world, subs)
        run_pass_seq(world, subs, lambda world,subs,n: update_birth_fine(world, startyear+i+1, n,1))
        run_pass_seq(world, subs, lambda world,subs,n: update_death_fine(world, startyear+i+1, n,i))
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
    popTotals = []
    numDivisions = 12
    for i in range(0,40*numDivisions):
        model1_compiler_pass(world, numDivisions)
        #model1_bd_comppass(world, numDivisions)
        year = i/numDivisions + 1
        if(year%5 == 0): #every 5 years
            projectedPops = scalar_data('projectedPopData.csv', 2010+int(year))
            #print(projectedPops)
            popTotals.append(np.append(populations(world), np.sum(populations(world))))
            popRegionalErrorData.append((populations(world) - projectedPops*1000)/(projectedPops*1000))
            popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))

        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    print(popRegionalErrorData)
    print(popTotalErrorData)
    pop2015 = scalar_data('regionPops.csv', 2015)
    savePops(popTotals, "sensitivity/populations_simple_bd.csv")

    #logging.info(np.sum(pop2015))
    #logging.info(np.sum(populations(world)))
    #logging.info(populations(world))

    #logging.info(pop2015 - populations(world))
    #logging.debug([usa for usa in world.regions if usa.name == 'USA'])

def saveLang(languageData, filename):
    top = ["country", "Arabic", "Bengali", "Catonese", "English", "French", "German", "Hausa", "Hindustani", "Italian",
           "Japonese", "Javanese", "Korean", "Malay", "Mandarin_Chinese", "Marathi", "Persian", "Portuguese", "Punjabi",
           "Russian", "Spanish", "Swahili", "Tamil", "Telugu", "Turkish", "Vietnamese", "Wu_Chinese"]
    regions = ["Angola", "ArabicMiddleEast", "ArabicWestAfrica", "AustrailiaNewZealand", "BalkanPeninsula", "Brazil",
               "BritishIsles", "Canada", "Caribbean", "CentralAmerica", "ChineseAsia", "EastAfrica", "EasternEurope",
               "FrenchEurope", "FrenchWestAfrica", "GermanEurope", "IndianSubcontinent", "ItalianEurope", "Japan",
               "Korea", "Madagascar", "Melanesia", "MiddleAfrica", "NordicCountries", "NorthAfrica", "PersianMiddleEast",
               "Portugal", "RussianAsia", "Somalia", "SoutheastAsia", "SouthernAfrica", "Spain", "SpanishSouthAmerica",
               "Tajikistan", "TurkishMiddleEast", "USA"]
    lDataList = languageData.tolist()
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(top)
        for index in range(0, len(regions)):
            lDataList[index].insert(0, regions[index])
            writer.writerow(lDataList[index])


def model1_5_percenterror():
    names = identifiers()
    language_names = lang_names('L1_Language_Data.csv')
    pops = scalar_data('regionPops.csv', 2010)
    brates = scalar_data('pr_birthRate.csv', 2010)
    #brates += 2.5
    drates = scalar_data('pr_deathRate.csv', 2010)
    logging.debug("CONTROLLER" + str(brates - drates))
    #logging.debug("CONTROLLER" + str(drates - ))
    #drates -= 2.5
    k_vals = mig_data('actual_r_migration2000_withk.csv')
    #logging.debug('K VALUES')
    #print(k_vals)
    #for i in range(0,len(k_vals)):
        #logging.debug(k_vals[i,:])
    L1s = lang_data('L1_Language_Data.csv')
    #logging.debug("LANG DATA: " + str(L1s))
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    logging.debug([cb for cb in world.regions if cb.name == 'Caribbean'])
    popRegionalErrorData = []
    popTotals = []
    popTotalErrorData = []
    popUNDifferenceData = []
    numDivisions = 12
    num5yearChuncks = 12
    for i in range(0,num5yearChuncks):
        model1_5_5yearpass_fine(world, numDivisions, 2010+5*i)
        projectedPops = scalar_data('projectedPopData.csv', 2010+5*(i+1))
        #print(projectedPops)
        popTotals.append(np.append(populations(world), np.sum(populations(world))))
        popRegionalErrorData.append(((populations(world) - projectedPops*1000)/(projectedPops*1000)))
        popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))
        popUNDifferenceData.append(np.append(((populations(world) - projectedPops * 1000) / (projectedPops * 1000)),
                                             (np.sum(populations(world)) - np.sum(projectedPops * 1000)) / np.sum(
                                                 projectedPops * 1000)))
        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    print(popRegionalErrorData)
    print(popTotalErrorData)
    popRegionalErrorData = np.transpose(np.asarray(popRegionalErrorData))
    #np.savetxt("prop_popRegionalError_10000.csv", popRegionalErrorData, delimiter=",")
    #np.savetxt("L1_1_2070.csv", L1s, delimiter=",")
    saveLang(L1s, "L1_1_2070.csv")
    saveLang(L2s, "L2_1_2070.csv")
    #np.savetxt("L1_1_2070.csv", L1s, delimiter=",")
    savePops(popTotals, "sensitivity/populations_update_2050_bd.csv")
    savePops(popUNDifferenceData, "model1pops/un_popdifference_bd.csv")

def model1_5_percenterror_2050():
    names = identifiers()
    language_names = lang_names('L1_Language_Data.csv')
    pops = scalar_data('projectedPopData.csv', 2050)*1000
    brates = scalar_data('pr_birthRate.csv', 2050)
    #brates += 2.5
    drates = scalar_data('pr_deathRate.csv', 2050)
    logging.debug("CONTROLLER" + str(brates - drates))
    #logging.debug("CONTROLLER" + str(drates - ))
    #drates -= 2.5
    k_vals = mig_data('actual_r_migration2000_withk.csv')
    #logging.debug('K VALUES')
    #print(k_vals)
    #for i in range(0,len(k_vals)):
        #logging.debug(k_vals[i,:])
    L1s = lang_data('L1_Language_Data.csv')
    #logging.debug("LANG DATA: " + str(L1s))
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    logging.debug([cb for cb in world.regions if cb.name == 'Caribbean'])
    popRegionalErrorData = []
    popTotals = []
    popTotalErrorData = []
    popUNDifferenceData = []
    numDivisions = 12
    num5yearChuncks = 4
    for i in range(0,num5yearChuncks):
        model1_5_5yearpass(world, numDivisions, 2050)
        projectedPops = scalar_data('projectedPopData.csv', 2050+5*(i+1))
        #print(projectedPops)
        popTotals.append(np.append(populations(world), np.sum(populations(world))))
        popRegionalErrorData.append(((populations(world) - projectedPops*1000)/(projectedPops*1000)))
        popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))
        popUNDifferenceData.append(np.append(((populations(world) - projectedPops*1000)/(projectedPops*1000)),
                                             (np.sum(populations(world)) - np.sum(projectedPops * 1000)) / np.sum(
                                                 projectedPops * 1000)))

        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    print(popRegionalErrorData)
    print(popTotalErrorData)
    popRegionalErrorData = np.transpose(np.asarray(popRegionalErrorData))
    #np.savetxt("prop_popRegionalError_10000.csv", popRegionalErrorData, delimiter=",")
    np.savetxt("L1_1_2070.csv", L1s, delimiter=",")
    savePops(popTotals, "sensitivity/populations_update_2050_bd.csv")
    savePops(popUNDifferenceData, "model1pops/un_popdifference_")

    #pop2015 = scalar_data('regionPops.csv', 2015)

    #logging.info(np.sum(pop2015))
    #logging.info(np.sum(populations(world)))
    #logging.info(populations(world))
    
    #logging.info([reg.L2 for reg in world.regions])
    #logging.info(pop2015 - populations(world))
    #logging.debug([usa for usa in world.regions if usa.name == 'USA'])
# get statistics
def populations(world):
    return np.array([reg.population for reg in world.regions])


regions = ["Angola", "ArabicMiddleEast", "ArabicWestAfrica", "AustrailiaNewZealand", "BalkanPeninsula", "Brazil",
           "BritishIsles", "Canada", "Caribbean", "CentralAmerica", "ChineseAsia", "EastAfrica", "EasternEurope",
           "FrenchEurope", "FrenchWestAfrica", "GermanEurope", "IndianSubcontinent", "ItalianEurope", "Japan",
           "Korea", "Madagascar", "Melanesia", "MiddleAfrica", "NordicCountries", "NorthAfrica", "PersianMiddleEast",
           "Portugal", "RussianAsia", "Somalia", "SoutheastAsia", "SouthernAfrica", "Spain", "SpanishSouthAmerica",
           "Tajikistan", "TurkishMiddleEast", "USA"]

def saveK(k_vals):
    top = ["region"] + regions
    with open('k_vals.csv', "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(top)
        kArray = k_vals.tolist()
        for i in range(0,len(kArray)):
            kArray[i].insert(0,regions[i])
            writer.writerow(kArray[i])


def savePops(popData, filename):
    top = ["year"] + regions + ["World"]
    years = [2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070]
    pDataList = popData
    #print(popData)
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(top)
        for index in range(0, len(pDataList)):
            pDataList[index] = np.insert(pDataList[index], 0, years[index])
            writer.writerow(pDataList[index])

def model2_percenterror():
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
    #logging.debug("LANG DATA: " + str(L1s))
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    logging.debug([cb for cb in world.regions if cb.name == 'Caribbean'])
    popRegionalErrorData = []
    popTotalErrorData = []
    popTotals = []
    numDivisions = 12
    num5yearChuncks = 12
    for i in range(0,num5yearChuncks):
        model2_5yearpass_fine(world, numDivisions, 2010+5*i)
        projectedPops = scalar_data('projectedPopData.csv', 2010+5*(i+1))
        #print(projectedPops)
        popTotals.append(np.append(populations(world), np.sum(populations(world))))
        popRegionalErrorData.append(((populations(world) - projectedPops*1000)/(projectedPops*1000)))
        popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))

        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    #print(popRegionalErrorData)
    print(popTotalErrorData)
    popRegionalErrorData = np.transpose(np.asarray(popRegionalErrorData))
    #np.savetxt("popRegionalError_12.csv", popRegionalErrorData, delimiter=",")
    #saveLang(L1s, "L1_2_2070.csv")
    #saveLang(L2s, "L2_2_2070.csv")
    savePops(popTotals, "sensitivity/populations_mbd.csv")
    saveLang(L1s, "L1_1_2070.csv")
    saveLang(L2s, "L2_1_2070.csv")
    #np.savetxt("L1_1_2070.csv", L1s, delimiter=",")
    #np.savetxt("L2_1_2070.csv", L2s, delimiter=",")
    
    #print(world.regions)

    #print(L2s)

    #pop2015 = scalar_data('regionPops.csv', 2015)

    #logging.info(np.sum(pop2015))
    #logging.info(np.sum(populations(world)))
    #logging.info(populations(world))

    #logging.info(pop2015 - populations(world))
    #logging.debug([usa for usa in world.regions if usa.name == 'USA'])
from pprintpp import pprint
def model2_sensitivity(j):
    names = identifiers()
    language_names = lang_names('L1_Language_Data.csv')
    pops = scalar_data('regionPops.csv', 2010)
    brates = scalar_data('r_birthRate.csv', 2010)
    drates = scalar_data('r_deathRate.csv', 2010)
    k_vals = mig_data('actual_r_migration2000_withk.csv')

    drates *= j
    
    #saveK(k_vals) 

    #k_vals *= j
    print(j)

    L1s = lang_data('L1_Language_Data.csv')
    #logging.debug("LANG DATA: " + str(L1s))
    L2s = lang_data('L2_Language_Data.csv')
    world = create_graph(names, pops, L1s, L2s, brates, drates, language_names, k_vals)
    #logging.debug(world)
    #logging.debug(np.sum(populations(world)))


    logging.debug([cb for cb in world.regions if cb.name == 'Caribbean'])
    popRegionalErrorData = []
    popTotalErrorData = []
    popTotals = []
    numDivisions = 12
    num5yearChuncks = 12
    for i in range(0,num5yearChuncks):
        model2_5yearpass_fine(world, numDivisions, 2010+5*i, j)
        projectedPops = scalar_data('projectedPopData.csv', 2010+5*(i+1))
        #print(projectedPops)
        popTotals.append(np.append(populations(world), np.sum(populations(world))))
        popRegionalErrorData.append(((populations(world) - projectedPops*1000)/(projectedPops*1000)))
        popTotalErrorData.append((np.sum(populations(world)) - np.sum(projectedPops*1000))/ np.sum(projectedPops*1000))

        #logging.debug(populations(world))
        #logging.debug(np.sum(populations(world)))
    #print(popRegionalErrorData)
    print(popTotalErrorData)
    popRegionalErrorData = np.transpose(np.asarray(popRegionalErrorData))
    #np.savetxt("popRegionalError_12.csv", popRegionalErrorData, delimiter=",")
    #saveLang(L1s, "sensitivity/L1_kvals_" + str(j) + ".csv")
    #saveLang(L2s, "sensitivity/L2_kvals_" + str(j) + ".csv")
    savePops(popTotals, "sensitivity/populations_drates_" + str(j) + ".csv")

# get statistics
def populations(world):
    return np.array([reg.population for reg in world.regions])

def main():
    #world = create_from_constants()
    
    #model1_compiler(world, subs, 1)
    #logging.info(world)
    #model1_test()
    #model1_5_percenterror()
    #model2_percenterror()
    for i in np.linspace(0.7,1.3,7):
        model2_sensitivity(i)

main()
