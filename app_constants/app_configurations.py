import configparser

config = configparser.ConfigParser()
config.read('conf/application.conf')

LOG_CONFIG_SECTION = "LOG"

class LOG:
    LOG_BASE_PATH = config.get(LOG_CONFIG_SECTION, 'base_path')
    LOG_LEVEL = config.get(LOG_CONFIG_SECTION, 'level')
    FILE_BACKUP_COUNT = config.get(LOG_CONFIG_SECTION, 'file_backup_count')
    FILE_BACKUP_SIZE = config.get(LOG_CONFIG_SECTION, 'max_log_file_size')
    FILE_NAME = LOG_BASE_PATH + config.get(LOG_CONFIG_SECTION, 'file_name')
    LOG_HANDLERS = config.get(LOG_CONFIG_SECTION, 'handlers')

