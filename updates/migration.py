
import logging

A = 0.86
B = 0.36

def migration(world, subs, n):
    regionFrom = world.regions[n]
#    logging.debug(regionFrom)
    edgesOut = world.edges[n]

    for i in range(0,len(world.regions)):
        k = edgesOut[i].immigration
        regionTo = world.regions[i]
        if (k == 0):
            if regionFrom.name == 'USA' or regionTo.name == 'USA':
                logging.debug('SKIPPED: ' + regionFrom.name + ' TO ' + regionTo.name)
            continue
        
        
        if regionFrom.name == 'USA' or regionTo.name == 'USA':
            logging.debug(regionFrom.population)

            logging.debug("POP FROM " + regionFrom.name + ": " + str(regionFrom.population))
            #logging.debug(regionFrom.population**A)
            logging.debug("POP TO " + regionTo.name + ": "  + str(regionTo.population))
            logging.debug("K: " + str(k))

        # calculate immigration
        imTotal = (regionFrom.population**A) * (regionTo.population**B) * k

        if regionFrom.name == 'USA' or regionTo.name == 'USA':
            logging.debug("IMTOTAL: " + str(imTotal))
        #logging.debug("IM" + str(imTotal))
        imTotal /= subs

        regionFrom.population = regionFrom.population - imTotal 
        regionTo.population = regionTo.population + imTotal

        L1moved = imTotal * (regionFrom.L1 / np.sum(regionFrom.L1))
        regionFrom.L1 -= L1Moved
        regionTo.L1 += L1Moved

        L2moved = imTotal * (regionFrom.L2 / np.sum(regionFrom.L2))
        regionFrom.L2 -= L2Moved
        regionTo.L2 += L2moved
