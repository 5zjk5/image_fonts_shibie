'''
腾讯云文字识别接口
https://cloud.tencent.com/act/event/ocrdemo#

接口文档
https://cloud.tencent.com/document/product/866/33526

快速接入文档
https://cloud.tencent.com/document/product/866/34681
'''


from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64
import jsonpath
import json


def open_img(path):
    '''
    输入路径，打开图片，base64 编码
    '''
    try:
        with open(path, 'rb') as f:  # 以二进制读取图片
            data = f.read()
            encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
            s = 'data:image/png;base64,'
            encodestr = s + str(encodestr)
            encodestr = encodestr.replace("b'", '')
        return encodestr
    except FileNotFoundError as e:
        return


def api_use(encodestr):
    '''
    调用 api 识别文图片上的文字
    '''
    try:
        cred = credential.Credential(你的密匙)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        req = models.GeneralBasicOCRRequest()
        params = '{"ImageBase64":"%s"}' % encodestr
        req.from_json_string(params)

        resp = client.GeneralBasicOCR(req)
        resp = resp.to_json_string()
        # print(resp)
        return resp

    except TencentCloudSDKException as err:
        print(err)


def get_text(resp):
    '''
    解析获得的 json 字符串，提取文本
    '''
    json_text = json.loads(resp)
    text = jsonpath.jsonpath(json_text, '$..DetectedText')
    text = ', '.join(text)
    return text


def main(path):
    '''
    主逻辑
    '''
    encodestr = open_img(path)
    if encodestr == None:
        text = '图片不存在，请输入正确的图片路径~~~'
        return text
    else:
        resp = api_use(encodestr)
        text = get_text(resp)
        return text


