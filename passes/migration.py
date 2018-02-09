
def migrations(world, n):
    regionFrom = world.region[n]
    edgesOut = world.edges[n]
    for i in range(0,n):
        immigration = edgesOut[i]
        if (immigration == 0):
            continue
        regionTo = world.region[i]
        newPopFrom = regionFrom.population - immigration
        newPopTo = regionTo.population + immigration

        regionFrom.L1 *= (newPopFrom / regionFrom.population)
        regionFrom.L2 *= (newPopFrom / regionFrom.population)
        regionFrom.population = newPopFrom

        regionTo.L1 *= (newPopTo / regionTo.population)
        regionTo.L2 *= (newPopTo / regionTo.population)
        regionTo.population = newPopTo
