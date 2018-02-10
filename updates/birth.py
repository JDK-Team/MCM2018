import logging

def birth(world, n):
    region = world.regions[n]

    logging.debug("BIRTH: " + region.name)

    region.L1 *= region.birthrate
    region.L2 *= region.birthrate
    region.population *= region.birthrate


# birth rate number is - births per thousand people.
