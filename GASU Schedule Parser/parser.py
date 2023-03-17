import asyncio
from helper_functions.utils import parse, clear_schedules

# 1. download files (bash)
#for fak in ADF AF FAU FIGX FSE SF; do for kval in b m; do curl -sS -O "http://doc.spbgasu.ru/Raspisanie/Raspisanie_${fak}_${kval}.xlsx"; done; done

# 2. set right schedules path
#schedule_files_path = "/var/www/robot/data/GASUS_Bot/GASU Schedule Parser/schedule_sheets/spring"
schedule_files_path = "/var/www/robot/data/GASUS_Bot/GASU Schedule Parser/schedule_sheets/fall"

#fixme check get_column_indexes_and_groupname_row_index() and modify if needed

# 3. parsing schedules:
# dryrun set to true - prints data to check
# dryrun set to false - loads data to Database
asyncio.get_event_loop().run_until_complete(clear_schedules())
asyncio.get_event_loop().run_until_complete(parse(schedule_files_path=schedule_files_path, dryrun=False))



# To CLEAR TABLE before uploading new schedules - RUN ME
#asyncio.get_event_loop().run_until_complete(clear_schedules())




