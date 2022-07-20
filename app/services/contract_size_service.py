from dotenv import load_dotenv
from os import environ
from core.endpoints import CONTRACTSIZE
from schemas.technical_analysis_schemas import GetContractSize
from common.common_helper import CommonHelper


load_dotenv
ENDPOINT = environ['SP_HOST_AND_PORT']
class ContractSize:
    __url = ENDPOINT + CONTRACTSIZE
    def __int__(self):
        pass

    @classmethod
    def __get_product_list(cls, request: GetContractSize):
        return CommonHelper.post_url(cls.__url, request)

    def get_contract_size(self, request:GetContractSize):
        res = self.__get_product_list(request)
        contract_size = res['data']['recordData']
        return contract_size