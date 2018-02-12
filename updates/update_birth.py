
from data_retrival.import_pop import scalar_data

def update_birth(world, year, n, i):
    region = world.regions[n]

    birthrates = scalar_data('pr_birthrate.csv', year)
    birthrates *= i

    region.birthrate = birthrates[n]
