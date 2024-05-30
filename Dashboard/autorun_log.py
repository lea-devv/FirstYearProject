from daily_changes import Daily_Changes

directory_location = ("D:/GrafiskDesign")
filechange_db_location = ("C:/Users/Administrator/Desktop/Dashboard/database/daily_filechanges.sqlite")

log_storage = Daily_Changes(filechange_db_location, directory_location, 7)
log_storage.log_changes()