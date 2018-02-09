
def death(world, n):
    region = world.regions[n]
    percentL1 = region.L1 / region.population
    percentL2 = region.L2 / region.population
    region.population *= region.deathrate
    region.L1 = percentL1*region.population
    region.L2 = percentL2*region.population
