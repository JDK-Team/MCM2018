
from data_retrival.import_pop import scalar_data
import logging

def update_death_fine(world, year, n):
    region = world.regions[n]
    
    if year == 2070:
        return

    partial = year % 5
    year = (year // 5) * 5

    deathrates_now = scalar_data('pr_deathrate.csv', year)
    if year == 2065:
        region.deathrate = deathrates_now[n]
        return
    
    deathrates_future = scalar_data('pr_deathrate.csv', year+5)


    diff = deathrates_future[n] - deathrates_now[n]
    region.deathrate = deathrates_now[n] + partial*(diff/5)

    logging.debug(partial)
    logging.debug(year)
    logging.debug(deathrates_now[n])
    logging.debug(deathrates_future[n])
    logging.debug(diff)
    logging.debug(region.deathrate)

