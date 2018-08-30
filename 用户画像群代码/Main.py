import BaseInfoAnalysis
import AppInfoAnalysis
import ServiceInfoAnalysis
import AppInfo
import BaseInfo
import ServiceInfo
AppInfo_path=AppInfo.data_path
BaseInfo_path=BaseInfo.data_path
ServiceInfo_path=ServiceInfo.data_path
import time
nums=len(AppInfo_path)
for i in range(nums):
    start_time=time.time()
    age=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_age()
    sex=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_sex()
    city=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_city()
    brand_model=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_brand_model()
    list_date=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_listing_date()
    list_price=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_listing_price()
    location=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[i]).get_location()
    app=AppInfoAnalysis.AppAnalysis(AppInfo_path[i]).get_appname()
    app_classify=AppInfoAnalysis.AppAnalysis(AppInfo_path[i]).get_classifyname()
    service=ServiceInfoAnalysis.ServiceAnalysis(ServiceInfo_path[i]).get_service()
    end_time=time.time()
    print(age)
    print(sex)
    print(city)
    print(brand_model)
    print(location)
    print(list_date)
    print(list_price)
    print(app)
    print(app_classify)
    print(service)
    print('程序运行时间为:%f'%(end_time-start_time))


