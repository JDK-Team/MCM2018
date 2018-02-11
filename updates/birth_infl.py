
from updates.influence import influence

def birth_infl(world, subs, n):

    region = world.regions[n]

    thousands = region.population / 1000
    nBirths = (thousands * region.birthrate) / subs
    region.population += nBirths

    region.L1 += nBirths*influence(region)
    
    
