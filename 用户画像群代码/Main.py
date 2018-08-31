import BaseInfoAnalysis
import AppInfoAnalysis
import ServiceInfoAnalysis
import AppInfo
import BaseInfo
import ServiceInfo
import time
import StatusMysql
while True:
    status=StatusMysql.GetStatus().get_status()
    if len(status)>0:
        AppInfo_path=AppInfo.App_data_path().get_path()
        BaseInfo_path=BaseInfo.Basic_data_path().get_path()
        ServiceInfo_path=ServiceInfo.Service_data_path().get_path()
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
                start_type=BaseInfoAnalysis.BaseAnalysis(BaseInfo_path[filenumber]).get_star_type()
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
                print(start_type)
                print('第%d文件程序运行时间为:%f'%((filenumber+1),(end_time-start_time)))
                print('*************\n*************\n第%d个文件数据分析完毕\n*************\n*************\n'%(filenumber+1))
        else:
            print('没有发现新文件，继续扫描')
        time.sleep(10)
    else:
        print('数据库状态码未发生变化，继续扫描')
        time.sleep(10)



