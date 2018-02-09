
def birth(world, n):
    region = world.regions[n]
    percentL1 = region.L1 / region.population
    percentL2 = region.L2 / region.population
    region.population *= region.birthrate
    region.L1 = percentL1*region.birthrate
    region.L2 = percentL2*region.birthrate

