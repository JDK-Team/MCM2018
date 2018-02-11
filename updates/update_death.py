
from data_retrival.import_pop import scalar_data

def update_death(world, year, n):
    region = world.regions[n]

    deathrates = scalar_data('pr_birthrate.csv', year)

    region.deathrate = deathrates[n]
