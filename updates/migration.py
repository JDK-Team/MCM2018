
A = 0.32
B = 0.86

def migration(world, n):
    regionFrom = world.regions[n]
    edgesOut = world.edges[n]
    for i in range(0,n):
        k = edgesOut[i].immigration
        if (k == 0):
            continue
        
        regionTo = world.regions[i]
        
        # calculate immigration
        imTotal = (regionTo.population**A) * (regionFrom.population**B) * k

        newPopFrom = regionFrom.population - imTotal 
        newPopTo = regionTo.population + imTotal

        regionFrom.L1 *= (newPopFrom / regionFrom.population)
        regionFrom.L2 *= (newPopFrom / regionFrom.population)
        regionFrom.population = newPopFrom

        regionTo.L1 *= (newPopTo / regionTo.population)
        regionTo.L2 *= (newPopTo / regionTo.population)
        regionTo.population = newPopTo
