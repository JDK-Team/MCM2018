
def death(world, n, rate):
    region = world.regions[n]
    percentL1 = region.L1 / region.population
    percentL2 = region.L2 / region.population
    region.population *= rate
    region.L1 = percentL1*rate
    region.L2 = percentL2*rate
