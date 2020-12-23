#coding=utf8
import time,json,logging
# from step_impl.pages.base_Page import Base_Page
# from step_impl.pages.sign_Code import Sign_Code
# from step_impl.pages.data_Yaml import Data_Yaml
# from step_impl.pages.log_module import Root_Log
from base_Page import Base_Page
from sign_Code import Sign_Code
from data_Yaml import Data_Yaml
from log_module import Root_Log
Root_Log.setup_logging()

class interfaceConfigParams:
    DataYaml = Data_Yaml()
    SignCode = Sign_Code()
    BasePage = Base_Page()
    

class Order_Page(interfaceConfigParams):

    def login(self):
        logging.info('login 接口 start...')
        try:
            get_url = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('login')['service']
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            url = '{}?timestamp={}&platform=9'.format(get_url,timestamp)
            logging.debug('url: %s' % url)
            headers = interfaceConfigParams.SignCode.get_Headers('post','login')
            logging.debug('headers: %s' % headers)
            params = interfaceConfigParams.DataYaml.getInterfaceParams('login')['params']
            logging.debug('params: %s' % params)
            response = interfaceConfigParams.BasePage.requests_Post(url,headers,params)
            logging.debug('response: %s' % response)
            accessToken = response['data']['accessToken']
            interfaceConfigParams.DataYaml.putTmpParams('accessToken',accessToken)
            logging.info('login 接口 end...')
            return True
        except Exception as e:
            return False
            logging.error('login 接口 failed:  errMessage[%s]' % e)

    def customerSearch(self):
        logging.info('customerSearch 接口 start...')
        try:
            geturl = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('customerSearch')['service']
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            accessToken = str(interfaceConfigParams.DataYaml.getTmpParams('accessToken'))
            headers = interfaceConfigParams.SignCode.get_Headers('get','customerSearch')
            params = interfaceConfigParams.DataYaml.getInterfaceYaml('customerSearch')['params']
            url = '{}?accessToken={}&timestamp={}&platform=9'.format(geturl,accessToken,timestamp)
            logging.debug('url: %s' % url)
            logging.debug('headers: %s' % headers)
            logging.debug('params: %s' % params)
            response = interfaceConfigParams.BasePage.requests_Get(url,headers,params)
            response = json.dumps(response)
            logging.debug('response: %s' % response)
            data = json.loads(response)['data']
            status = json.loads(response)['status']
            if status == 'success':
                for line in range(0,len(data)):
                    if data[line]['mobile'] == '18613137446':
                        logging.debug('customerId: %s' % data[line]['id'])
                        interfaceConfigParams.DataYaml.putTmpParams('customerId',data[line]['id'])
                        logging.info('customerSearch 接口 end...')
                        return True
            else:
                logging.error('customerSearch 接口 failed:  errMessage[%s]' % json.loads(response))
                return False
        except Exception as e:
            logging.error('customerSearch 接口 failed:  errMessage[%s]' % e)
            return False
    
    def customerDetail(self):
        logging.info('customerDetail 接口 start...')
        try:
            geturl = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('customerDetail')['service']
            ids = interfaceConfigParams.DataYaml.getTmpParams('customerId')
            geturl = geturl.format(ids=ids)
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            accessToken = str(interfaceConfigParams.DataYaml.getTmpParams('accessToken'))
            headers = interfaceConfigParams.SignCode.get_Headers('get','customerDetail')
            params = interfaceConfigParams.DataYaml.getInterfaceYaml('customerDetail')['params']
            url = '{}?accessToken={}&timestamp={}&platform=9'.format(geturl,accessToken,timestamp)
            logging.debug('url: %s' % url)
            logging.debug('headers: %s' % headers)
            logging.debug('params: %s' % params)
            response = interfaceConfigParams.BasePage.requests_Get(url,headers,params)
            response = json.dumps(response)
            logging.debug('response: %s' % response)
            data = json.loads(response)['data']['cars']
            status = json.loads(response)['status']
            if status == 'success':
                interfaceConfigParams.DataYaml.putParamsOverWrite('customerInfoBO.yaml','customerInfoBO',json.loads(response)['data'])
                for line in range(0,len(data)):
                    if data[line]['carNo'] == '川C66666':
                        logging.debug('carModelId: %s' % data[line]['carModelId'])
                        interfaceConfigParams.DataYaml.putTmpParams('carModelId',data[line]['carModelId'])
                        interfaceConfigParams.DataYaml.putParamsOverWrite('orderCarBO.yaml','orderCarBO',data[line])
                        logging.info('customerDetail 接口 end...')
                        return True
            else:
                logging.error('customerDetail 接口 failed:  errMessage[%s]' % json.loads(response))
                return False
        except Exception as e:
            logging.error('customerDetail 接口 failed:  errMessage[%s]' % e)
            return False
               
    def customerProduct(self):
        logging.info('customerProduct 接口 start...')
        try:
            geturl = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('customerProduct')['service']
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            accessToken = str(interfaceConfigParams.DataYaml.getTmpParams('accessToken'))
            headers = interfaceConfigParams.SignCode.get_Headers('get','customerProduct')
            params = interfaceConfigParams.DataYaml.getInterfaceYaml('customerProduct')['params']
            params['customerId'] = interfaceConfigParams.DataYaml.getTmpParams('customerId')
            url = '{}?accessToken={}&timestamp={}&platform=9'.format(geturl,accessToken,timestamp)
            response = interfaceConfigParams.BasePage.requests_Get(url,headers,params)
            # response = json.dumps(response)
            logging.debug('url: %s' % url)
            logging.debug('headers: %s' % headers)
            logging.debug('params: %s' % params)
            logging.debug('response: %s' % response)
            if response['status'] == 'success':
                data = response['data'][0]['products']
                # print(data)
                interfaceConfigParams.DataYaml.putParamsOverWrite('productList.yaml','productList',data)
                logging.info('customerProduct 接口 end...')
                return True
            else:
                logging.error('customerProduct 接口 failed:  errMessage[%s]' % response)
                return False
        except Exception as e:
            logging.error('customerProduct 接口 failed:  errMessage[%s]' % e)
            return False
            
    def queryPackage(self):
        logging.info('queryPackage 接口 start...')
        try:
            geturl = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('queryPackage')['service']
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            accessToken = str(interfaceConfigParams.DataYaml.getTmpParams('accessToken'))
            headers = interfaceConfigParams.SignCode.get_Headers('get','queryPackage')
            params = interfaceConfigParams.DataYaml.getInterfaceYaml('queryPackage')['params']
            params['carModelId'] = interfaceConfigParams.DataYaml.getTmpParams('carModelId')
            url = '{}?accessToken={}&timestamp={}&platform=9'.format(geturl,accessToken,timestamp)
            response = interfaceConfigParams.BasePage.requests_Get(url,headers,params)
            logging.debug('url: %s' % url)
            logging.debug('headers: %s' % headers)
            logging.debug('params: %s' % params)
            logging.debug('response: %s' % response)
            response_status = response['status']
            if response_status == 'success':
                logging.info('queryPackage 接口 end...')
                return True
            else:
                logging.error('queryPackage 接口 failed:  errMessage[%s]' % response)
                return False
        except Exception as e:
            logging.error('queryPackage 接口 failed:  errMessage[%s]' % e)
            return False
            
    def queryProduct(self):
        logging.info('queryProduct 接口 start...')
        try:
            geturl = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('queryProduct')['service']
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            accessToken = str(interfaceConfigParams.DataYaml.getTmpParams('accessToken'))
            headers = interfaceConfigParams.SignCode.get_Headers('post','queryProduct')
            params = interfaceConfigParams.DataYaml.getInterfaceYaml('queryProduct')['params']
            params['carModelId'] = interfaceConfigParams.DataYaml.getTmpParams('carModelId')
            url = '{}?accessToken={}&timestamp={}&platform=9'.format(geturl,accessToken,timestamp)
            response = interfaceConfigParams.BasePage.requests_Post(url,headers,params)
            logging.debug('url: %s' % url)
            logging.debug('headers: %s' % headers)
            logging.debug('params: %s' % params)
            logging.debug('response: %s' % response)
            response_status = response['status']
            if response_status == 'success':
                logging.info('queryProduct 接口 end...')
                return True
            else:
                logging.error('queryProduct 接口 failed:  errMessage[%s]' % response)
                return False
        except Exception as e:
            logging.error('queryProduct 接口 failed:  errMessage[%s]' % e)
            logging.error('queryProduct 接口 failed:  errMessage[%s]' % response)
            return False

    def queryLocal(self):
        logging.info('queryLocal 接口 start...')
        try:
            geturl = interfaceConfigParams.DataYaml.getInterfaceHost() + interfaceConfigParams.DataYaml.getInterfaceParams('queryLocal')['service']
            timestamp = str(interfaceConfigParams.DataYaml.getTmpParams('timestamp'))
            accessToken = str(interfaceConfigParams.DataYaml.getTmpParams('accessToken'))
            headers = interfaceConfigParams.SignCode.get_Headers('post','queryLocal')
            params = interfaceConfigParams.DataYaml.getInterfaceYaml('queryLocal')['params']
            params['carModelId'] = interfaceConfigParams.DataYaml.getTmpParams('carModelId')
            url = '{}?accessToken={}&timestamp={}&platform=9'.format(geturl,accessToken,timestamp)
            response = interfaceConfigParams.BasePage.requests_Post(url,headers,params)
            logging.debug('url: %s' % url)
            logging.debug('headers: %s' % headers)
            logging.debug('params: %s' % params)
            logging.debug('response: %s' % response)
            response_status = response['status']
            if response_status == 'success':
                logging.info('queryLocal 接口 end...')
                return True
            else:
                logging.error('queryLocal 接口 failed:  errMessage[%s]' % response)
                return False
        except Exception as e:
            logging.error('queryLocal 接口 failed:  errMessage[%s]' % e)
            logging.error('queryLocal 接口 failed:  errMessage[%s]' % response)
            return False


if __name__ == "__main__":
    # Order_Page().login()
    # Order_Page().customerSearch()
    Order_Page().customerDetail()
    # Order_Page().customerProduct()
    # Order_Page().queryPackage()
    # Order_Page().queryProduct()
    # Order_Page().queryLocal()