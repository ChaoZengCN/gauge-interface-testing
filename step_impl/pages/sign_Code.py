#coding=utf8
import hashlib,base64
import time,json,logging
import urllib.parse
# from step_impl.pages.data_Yaml import Data_Yaml
# from step_impl.pages.base_Page import Base_Page
# from step_impl.pages.log_module import Root_Log
from data_Yaml import Data_Yaml
from base_Page import Base_Page
from log_module import Root_Log
Root_Log.setup_logging()

class Sign_Code(object):
    ''' sign加密'''
    def __init__(self):
        self.BasePage = Base_Page()
        self.DataYaml = Data_Yaml()
        self.DataYaml.putTmpParams('timestamp',int(round((time.time()) * 1000)))

    def sign_Data_Get(self,mode,value):
        '''
        加密前参数组装 
            mode=请求方式（post,get) 
            value=接口名
        clientId 服务端提供 ;clientScret 固定参数
        '''
        try:
            clientId = self.DataYaml.getInterfaceYaml('sign')['clientId']
            clientScret = self.DataYaml.getInterfaceYaml('sign')['clientScret']
            platform = self.DataYaml.getInterfaceYaml('sign')['platform']
            timestamp = self.DataYaml.getTmpParams('timestamp')
            json_body = self.BasePage.json_Body(mode,value)
            
            if value == 'login' and mode == 'post':
                signCode = 'timestamp={}&platform={}+{}+{}'.format(str(timestamp),str(platform),json_body,str(clientScret))
            elif mode == 'get':
                signCode = 'accessToken={}&timestamp={}&platform={}&{}'.format(str(self.DataYaml.getTmpParams('accessToken')),str(timestamp),str(platform),json_body)
            elif mode == 'post':
                signCode = 'accessToken={}&timestamp={}&platform={}+{}'.format(str(self.DataYaml.getTmpParams('accessToken')),str(timestamp),str(platform),json_body)
            logging.info('加密参数拼装完成...')
            return signCode 
        except Exception as e:
            logging.error('加密参数组装错误: %s' % e)

    def encrypt_Code(self,mode,value):   
        '''MD5加密'''
        try:
            data = self.sign_Data_Get(mode,value)
            logging.debug('Sign加密前:%s' % data)
            md5 = hashlib.md5()
            md5.update(data.encode('utf8'))
            # encodeStr = md5.hexdigest().lower()
            encodeStr = md5.hexdigest()
            logging.debug('Sign加密后:%s' % encodeStr)
            return encodeStr
        except Exception as e:
            logging.error('MD5加密失败 %s' % e)
    
    def get_Headers(self,mode,value):  
        '''组装消息头'''
        try:
            if mode == 'post':
                values1 = ['clientId','signcode','content-type'] 
                clientId = self.DataYaml.getInterfaceParams('sign')['clientId']
                data = self.encrypt_Code(mode,value)
                values2 = [clientId,data,'application/json']
                signcode = dict(zip(values1,values2))
            elif mode == 'get':
                values1 = ['clientId','signcode'] 
                clientId = self.DataYaml.getInterfaceParams('sign')['clientId']
                data = self.encrypt_Code(mode,value)
                values2 = [clientId,data]
                signcode = dict(zip(values1,values2))
            logging.info('Headers拼装完成...')
            return signcode 
        except Exception as e:
            logging.error('Headers 组装失败 %s' % e)
    


# if __name__ == "__main__":
#     # print(Sign_Code().encrypt_Code('customerSearch'))
#     Sign_Code().encrypt_Code('login')
    
