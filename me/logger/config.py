import logging as log

# Default (applied if the class itself doesn't chose it level)
PROJECT_LOG_LEVEL = log.INFO

# Any log under FORCE_MIN_LOG_LEVEL is NOT printed (except if FORCE_MIN_LOG_LEVEL is NOTSET)
FORCE_MIN_LOG_LEVEL = log.NOTSET

# Any log above or equal to FORCE_MAX_LOG_LEVEL is printed (except if FORCE_MAX_LOG_LEVEL is NOTSET)
FORCE_MAX_LOG_LEVEL = log.WARNING


