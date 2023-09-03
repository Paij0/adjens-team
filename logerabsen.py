import spdlog
# SPDLOG C++ wrapper for python
class SPD:
    logger = ''

    @classmethod
    def set_dir(cls, name, dir, level):
        cls.logger = spdlog.FileLogger(name, dir)
        if level == 'DEBUG' or level == 'debug':
          cls.logger.set_level(spdlog.LogLevel.DEBUG)
        elif level == 'INFO' or level == 'info':
          cls.logger.set_level(spdlog.LogLevel.INFO)
        
    @classmethod
    def debug(cls, text):
        cls.logger.debug(text)
    
    @classmethod
    def info(cls, text):
        cls.logger.info(text)