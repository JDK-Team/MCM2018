
from data_retrival.import_pop import scalar_data
import logging

def update_birth_fine(world, year, n, i):
    region = world.regions[n]

    if year == 2070:
        return

    partial = year % 5
    year = (year // 5) * 5
    
    birthrates_now = scalar_data('pr_birthrate.csv', year)
    birthrates_now *= i
    if year == 2065:
        region.birthrate = birthrates_now[n]
        return

    birthrates_future = scalar_data('pr_birthrate.csv', year+5)
    birthrates_future *= i

    diff = birthrates_future[n] - birthrates_now[n]
    region.birthrate = birthrates_now[n] + partial*(diff/5)

    logging.debug(i)
    logging.debug(partial)
    logging.debug(year)
    logging.debug(birthrates_now[n])
    logging.debug(birthrates_future[n])
#    logging.debug(diff)
#    logging.debug(region.birthrate)
