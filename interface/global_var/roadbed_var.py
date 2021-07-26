"""
服务后台接口/
"""
from interface.global_var.global_var_model import http_pex
"""
筑路信息
"""
technologyLevel = ['沥青上面层','沥青中面层','沥青下面层']
company_admin_password = '5JSjZ8'
company_admin_phone = '18172163341'
company_name = '飞利信网络有限公司'
ProjectTypeName='土方项目'
ProjecName='项目名称_eYAgHl5bK'
"""接口信息"""
#添加工艺层级
company_addLevel=http_pex+"api/iot-roadbed/v1/roadbed/technologyLevel/add"
#添加摊铺属性
company_addStand=http_pex+"api/iot-roadbed/v1/roadbed/technologyStand/add"
