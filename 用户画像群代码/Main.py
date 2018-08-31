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
filenums=len(AppInfo_path)
if filenums :
    for filenumber in range(filenums):
        start_time=time.time()
        age=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_age()
        sex=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_sex()
        city=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_city()
        brand_model=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_brand_model()
        list_date=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_listing_date()
        list_price=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_listing_price()
        location=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_location()
        app=AppInfoAnalysis.AppAnalysis(AppInfo_path[filenumber]).get_appname()
        app_classify=AppInfoAnalysis.AppAnalysis(AppInfo_path[filenumber]).get_classifyname()
        service=ServiceInfoAnalysis.ServiceAnalysis(ServiceInfo_path[filenumber]).get_service()
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
else:
    print('没有发现新文件，继续扫描')


