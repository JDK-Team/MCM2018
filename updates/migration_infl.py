
import numpy as np
from updates.influence import influence

A = 0.86
B = 0.36

def migration_infl(world, subs, n): 
    regionFrom = world.regions[n]

    edgesOut = world.edges[n]
    for i in range(0,len(world.regions)):
        k = edgesOut[i].immigration
        regionTo = world.regions[i]
        if (k == 0): 
            continue
        # calculate immigration
        imTotal = (regionFrom.population**A) * (regionTo.population**B) * k

        imTotal /= subs

        regionFrom.population = regionFrom.population - imTotal
        regionTo.population = regionTo.population + imTotal

        L1_moved = imTotal * (regionFrom.L1 / regionFrom.population)
        if 0 < k:
            regionFrom.L1 -= L1_moved

        regionTo.L1 += L1_moved

        regionFrom.L1[regionFrom.L1 < 0] = 0
        regionTo.L1[regionTo.L1 < 0] = 0

        L2_moved = imTotal * (regionFrom.L2 / regionFrom.population)
        if 0 < k:
            regionFrom.L2 -= L2_moved
        regionTo.L2 += L2_moved

        regionTo.L2 += imTotal * influence(regionTo)

        regionFrom.L2[regionFrom.L2 < 0] = 0
        regionTo.L2[regionTo.L2 < 0] = 0
