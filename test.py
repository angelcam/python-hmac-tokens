from logger import log, INFO

log.start("myAppName")
log.set_min_level(INFO)
log.set_output_writing(True)
# log.set_loggly('07e7166c-bd6d-459d-8cd0-4bd4333f04fb', 'python')
log.start('test.py')

log.info("This is log message.", camera_id=123)
print('Done')
