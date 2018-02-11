
from data_retrival.import_pop import scalar_data

def update_birth(world, year, n):
    region = world.regions[n]

    birthrates = scalar_data('pr_birthrate.csv', year)
    #birthrates += 2.5

    region.birthrate = birthrates[n]
