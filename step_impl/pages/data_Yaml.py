#coding=utf8
import time,logging,json
from ruamel import yaml
# from step_impl.pages.log_module import Root_Log
from log_module import Root_Log
Root_Log.setup_logging()

class ConfigLoad:
    '''读取config文件信息'''
    path = 'F:/InterFace/CheShiFu/config/'     #文件地址
    config_file = 'config.yaml'              #config配置文件
    # interface_name = 'filename_interface'     #接口
    # tmp_name = 'filename_tmp'                 #临时文件
    # logger_name = 'filename_logger'           #日志
    # c_p_details_name = 'customerProduct_details'  #客户已购套餐

    def file_config_Load(self,filename):     #获取接口文件名
        with open(ConfigLoad.path + ConfigLoad.config_file,'r',encoding='UTF-8') as f:
            self.data = yaml.safe_load(f.read())
        return self.data[filename]

class Data_Yaml(object):   

    def __init__(self):
        # self.values =  values
        self.path = ConfigLoad.path
        self.interfaceConfig = ConfigLoad().file_config_Load('filename_interface')
        self.tmpConfig = ConfigLoad().file_config_Load('filename_tmp')
        self.loggerConfig = ConfigLoad().file_config_Load('filename_logger')
        # self.CPDetailsConfig = ConfigLoad().file_config_Load('customerProduct_details')

    def getInterfaceYaml(self,values):   #读取接口文件对应字段
        try:
            with open(self.path+self.interfaceConfig,'r',encoding='UTF-8') as f:
                self.data = yaml.safe_load(f.read())
            return self.data[values]
        except Exception as e:
            logging.error('getInterfaceYaml失败... :%s' % e)


    def getInterfaceHost(self):   #获取 host 
        try:
            host = self.getInterfaceYaml('host')
            return host
        except:
            logging.error('获取HOST失败...')

    def getInterfaceParams(self,interface):  #获取 接口文件内容
        try:
            data = self.getInterfaceYaml(interface)
            return data
        except:
            logging.error('getInterfaceParams失败...')

    def putTmpParams(self,name,value): #更新tmp文件
        try:
            with open(self.path+self.tmpConfig,'r',encoding='UTF-8') as f:
                data = yaml.safe_load(f.read())
            data[name] = value
            with open(self.path+self.tmpConfig,'w',encoding='UTF-8') as f:
                yaml.dump(data,f,Dumper=yaml.RoundTripDumper)
        except:
            logging.error('更新TMP文件失败...')

    def getTmpParams(self,name): #获取tmp文件指定NAME内容
        with open(self.path+self.tmpConfig,'r',encoding='UTF-8') as f:
            data = yaml.safe_load(f.read())
        try:
            return data[name]
        except:
            return None
    
    def putParamsOverWrite(self,filename,params,data):
        try:
            more = {params:data}
            with open(self.path+filename,'w',encoding='UTF-8') as f:
                yaml.dump(more,f,Dumper=yaml.RoundTripDumper)
        except:
            logging.error('更新 %s 文件失败...' % filename)


if __name__ == "__main__":
    # print(Data_Yaml().getTmpParams('timestamp'))
    # Data_Yaml().putTmpParams('timestamp',11111)
    # Data_Yaml().putParams('test.yaml','test')
    print(Data_Yaml().getInterfaceParams('login'))