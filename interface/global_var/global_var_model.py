"""
服务平台用户信息
"""
company_admin_userName = 'vJSXgNDaMi9'
company_admin_password = '5JSjZ8'
company_admin_phone = '18172163341'
company_name = '飞利信网络有限公司'
ProjectTypeName='土方项目'
ProjecName='项目名称_eYAgHl5bK'
"""
管理后台用户信息
"""
admin_userName = 'admin'  # 管理后台账号
admin_password = '123456'  # 管理后台密码

"""服务平台"""
http_pex = 'http://47.105.124.12:86/'
headers = {"Accept": "application/json,text/plain,*/*",
           'Referer': 'http://47.105.124.12:86/',
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
           'Content-Type': 'application/json;charset=UTF-8'
           }
"""管理平台"""
admin_http_pex = 'http://47.105.124.12:84/'
admin_headers = {"Accept": "application/json,text/plain,*/*",
                 'Referer': 'http://47.105.124.12:84/',
                 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
                 'Content-Type': 'application/json;charset=UTF-8'
                 }
"""
服务后台接口
"""
# 注册-获取验证码
getmessage = http_pex + "api/iot-device/v1/manage/system/company/getmessage"
# 注册-验证验证码
checkMessage = http_pex + "api/iot-device/v1/manage/system/company/checkMessage"
# 根据手机号获取用户信息
getUser = http_pex + "api/v1/manage/system/company/getUser?"
# 注册-添加用户
addUser = http_pex + "api/iot-device/v1/manage/system/company/addUser"
# 注册-提交审核
coment = http_pex + "api/iot-device/v1/manage/system/company/coment"
# 登录
company_login = http_pex + "api/iot-base-server/v1/wx/user/login"
# 获取菜单权限
company_menu = http_pex + "api/iot-device/v1/manage/companyRole/public/companyTreeMenu"
# 创建角色
company_roleAdd = http_pex + "api/iot-device/v1/manage/companyRole/add"
# 查找角色
company_roleFind = http_pex + "api/iot-device/v1/manage/companyRole/getList"
# 创建单位
company_UnitsAdd = http_pex + "api/iot-device/v1/manage/constructUnits/add"
# 查找单位
company_UnitsFind = http_pex + "api/iot-device/v1/manage/constructUnits/getList"
# 创建用户api/iot-base-server/v2/system/projectManger/selectProjectTypeInfo
company_userAdd = http_pex + "api/iot-device/v1/manage/company/user/add"
# 获取项目类别
company_ProjectType = http_pex + "api/iot-base-server/v2/system/projectManger/selectProjectTypeInfo"
#获取省
company_Province = http_pex + "api/iot-base-server/v2/system/province/selectProvince"
#获取市
company_City = http_pex + "api/iot-base-server/v2/system/province/selectCityByProvinceCode"
#获取单位
company_Units = http_pex + "api/iot-device/v1/manage/constructUnits/getList"
#获取设备
company_Devices = http_pex + "api/iot-device/v1/manage/ProjectInfo/getDeviceTypeNOtSelect?deviceName="
#创建项目
company_AddProject = http_pex + "api/iot-device/v1/manage/ProjectInfo/addProjectInfo"
#获取项目
company_ProjectList = http_pex + "api/iot-device/v1/manage/ProjectInfo/getProjectListByUid"
"""
管理后台接口
"""
# 管理后台登录
login = admin_http_pex + "api/iot-base-server/v2/system/homePage/login"
# 获取菜单权限
menu = admin_http_pex + 'api/iot-base-server/v2/system/menuManage/selectMenu'
# 添加角色
roleAdd = admin_http_pex + "api/iot-base-server/v2/system/role/add"
# 查找角色id
findRole = admin_http_pex + "api/iot-base-server/v2/system/role/list/page"
# 查找待审核企业id
findCompany = admin_http_pex + "api/iot-base-server/v2/system/applyCompany/applyCompanyReviewList"
# 审核企业
checkApplyCompany = admin_http_pex + "api/iot-base-server/v2/system/applyCompany/auditApplyCompany"
# 创建项目类别
addProjectType = admin_http_pex + "api/iot-base-server/v2/system/projectManger/addProjectType"
# 查找项目类别
findProjectType = admin_http_pex + "api/iot-base-server/v2/system/projectManger/selectProjectTypeInfo"
# 创建产品类别
addProduct = admin_http_pex + "api/iot-base-server/v2/system/productManger/addProduct"
# 查找项目类别api/iot-base-server/v2/system/deviceModel/add
findProduct = admin_http_pex + "api/iot-base-server/v2/system/productManger/selectProduct"
# 创建厂商产品型号
addDeviceModel = admin_http_pex + "api/iot-base-server/v2/system/deviceModel/add"
# 查找厂商产品型号api/iot-base-server/v2/system/deviceParts/add
findDeviceModel = admin_http_pex + "api/iot-base-server/v2/system/public/code/getModelList"
# 创建设备部件
addDeviceParts = admin_http_pex + "api/iot-base-server/v2/system/deviceParts/add"
# 查找设备部件
findDeviceParts = admin_http_pex + "api/iot-base-server/v2/system/deviceParts/list/page"
# 创建设备
addDevice = admin_http_pex + "api/iot-base-server/v2/system/deviceBaseInfo/add"
# 查找设备
findDevice = admin_http_pex + "api/iot-base-server/v2/system/deviceBaseInfo/list/page"
# 创建终端
addTerminal = admin_http_pex + "api/iot-base-server/v2/system/terminal/add"
# 企业列表查找企业
findCheckedCompany = admin_http_pex + "api/iot-base-server/v2/system/list/page"
# 企业列表查找设备
findBindDevicePage = admin_http_pex + "api/iot-base-server/v2/system/company/BindDevicePage"
# 数据授权
bindTerminal = admin_http_pex + "api/iot-base-server/v2/system/batchBind/device"
