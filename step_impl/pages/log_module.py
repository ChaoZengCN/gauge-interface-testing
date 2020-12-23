#coding=utf8
import yaml,os
import logging.config
# from data_Yaml import ConfigLoad

class Root_Log:
    def setup_logging(default_path = "",default_level = logging.INFO,env_key = "LOG_CFG"):
        path = default_path
        # value = ConfigLoad.path + ConfigLoad().logger_config_Load()
        value = 'F:/InterFace/CheShiFu/config/logger.yaml'
        if value:
            path = value
        if os.path.exists(path):
            with open(path,'r',encoding='UTF-8') as f:
                config = yaml.load(f.read(),Loader=yaml.FullLoader)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level = default_level)

if __name__ == "__main__":
    Root_Log.setup_logging()
    logging.info("start func")
    logging.warning("exec func")
    logging.debug("end func")