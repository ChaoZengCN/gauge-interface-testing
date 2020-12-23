#coding=utf8
import requests,json,urllib,logging
# from step_impl.pages.data_Yaml import Data_Yaml
# from step_impl.pages.log_module import Root_Log
from data_Yaml import Data_Yaml
from log_module import Root_Log
Root_Log.setup_logging()
requests.packages.urllib3.disable_warnings()

class Base_Page(object):

    def __init__(self):
        self.DataYaml = Data_Yaml()
    
    def requests_Get(self,url,headers,params):  # GET 方法封装

        try:
            respond = requests.get(url=url,headers=headers,params=params,verify=False)
            text = respond.json()
            return text
        except Exception as e:
            print(e)

    def requests_Post(self,url,headers,data):  # POST 方法封装
        try:
            respond = requests.post(url,headers=headers,data=json.dumps(data),verify=False)
            # respond.raise_for_status()
            return respond.json()
        except Exception as e:
            print(e)

    def json_Body(self,mode,value):    #获取接口json串
        try:
            body = self.DataYaml.getInterfaceParams(value)['params']
            bodyKeys = list(body.keys())
            for line in range(0,len(bodyKeys)):  #将临时参数value传入body
                if  self.DataYaml.getTmpParams(bodyKeys[line]) is not None :
                    body[bodyKeys[line]] = self.DataYaml.getTmpParams(bodyKeys[line])
            data = json.dumps(body,ensure_ascii=False)
            if mode == 'get':
                data = json.loads(data)
                data = urllib.parse.urlencode(data)
            logging.info('jsonBody参数组装完成...')
            return data
        except Exception as e:
            logging.error('jsonBody组装失败: %s' % e)  

if __name__ == "__main__":
    print(Base_Page().json_Body('post',True,'customerProduct'))