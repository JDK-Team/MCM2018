
import logging
import numpy as np

A = 0.86
B = 0.36

def migration(world, subs, n):
    regionFrom = world.regions[n]
    #logging.debug(regionFrom)
    edgesOut = world.edges[n]

    for i in range(0,len(world.regions)):
        k = edgesOut[i].immigration
        regionTo = world.regions[i]
        if (k == 0):
            #if regionFrom.name == 'RussianAsia' or regionTo.name == 'RussianAsia':
                #logging.debug('SKIPPED: ' + regionFrom.name + ' TO ' + regionTo.name)
            continue
        
        # calculate immigration
        imTotal = (regionFrom.population**A) * (regionTo.population**B) * k
        
        #if regionFrom.name == 'Caribbean' or regionTo.name == 'Caribbean':
        #    logging.debug(regionFrom.population)

        #    logging.debug("POP FROM " + regionFrom.name + ": " + str(regionFrom.population))
            #logging.debug(regionFrom.population**A)
        #    logging.debug("POP TO " + regionTo.name + ": "  + str(regionTo.population))
        #    logging.debug("K: " + str(k))


        #if regionFrom.name == 'Caribbean' or regionTo.name == 'Caribbean':
            #continue
            #logging.debug("IMTOTAL: " + str(imTotal))
            #logging.debug("IM" + str(imTotal))
        imTotal /= subs

        regionFrom.population = regionFrom.population - imTotal 
        regionTo.population = regionTo.population + imTotal

        if np.sum(regionFrom.L1) <= 0:
            logging.debug("BAD L1 DATA: " + regionFrom.name + str(regionFrom.L1))
            #continue

        if np.sum(regionFrom.L2) <= 0:
            logging.debug("BAD L2 DATA: " + regionFrom.name + str(regionFrom.L2))
            #continue

        #if regionFrom.name == 'Caribbean':
        #    logging.debug("L1: " + str(regionFrom.L1))
        #if regionTo.name == 'Caribbean':
        #    logging.debug("L1: " + str(regionTo.L1))

        L1_moved = imTotal * (regionFrom.L1 / regionFrom.population)#np.sum(regionFrom.L1))
        #if regionFrom.name == 'Caribbean':
        #    logging.debug(L1_moved)
        #if regionTo.name == 'Caribbean':
        #    logging.debug(L1_moved)
        regionFrom.L1 -= L1_moved
        #regionFrom.L1[regionFrom.L1 < 0] = 0
        regionTo.L1 += L1_moved
        #regionTo.L1[regionTo.L1 < 0] = 0
        #if regionFrom.name == 'Caribbean':
            #logging.debug("L1 AFTER: " + str(regionFrom.L1))
        #if regionTo.name == 'Caribbean':
            #logging.debug("L1 AFTER: " + str(regionTo.L1))

        L2_moved = imTotal * (regionFrom.L2 / regionFrom.population)#np.sum(regionFrom.L2))
        regionFrom.L2 -= L2_moved
        #regionFrom.L2[regionFrom.L2 < 0] = 0
        regionTo.L2 += L2_moved
