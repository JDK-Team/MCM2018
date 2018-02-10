
import logging

A = 0.86
B = 0.36

def migration(world, subs, n):
    regionFrom = world.regions[n]
#    logging.debug(regionFrom)
    edgesOut = world.edges[n]
    for i in range(0,n):
        k = edgesOut[i].immigration
        if (k == 0):
            continue
        
        regionTo = world.regions[i]
        
        # calculate immigration
        #logging.debug("POP FROM: " + str(regionFrom.population))
        #logging.debug(regionFrom.population**A)
        #logging.debug("POP TO: " + str(regionTo.population))
        #logging.debug(k)
        imTotal = (regionFrom.population**A) * (regionTo.population**B) * k

        #logging.debug("IM" + str(imTotal))
        imTotal /= subs

        newPopFrom = regionFrom.population - imTotal 
        newPopTo = regionTo.population + imTotal

        regionFrom.L1 *= (newPopFrom / regionFrom.population)
        regionFrom.L2 *= (newPopFrom / regionFrom.population)
        regionFrom.population = newPopFrom

        regionTo.L1 *= (newPopTo / regionTo.population)
        regionTo.L2 *= (newPopTo / regionTo.population)
        regionTo.population = newPopTo
