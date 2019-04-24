//建立L1_注册事件表
create table if not exists `sinaif_commerce_dm.mid_register_events`(
    `phone` string comment '手机号',
    `deviceid` string comment '设备ID',
    `accountid` string comment '第三方ID',
    `register_time` string comment '注册时间',
    `register_channel` string comment '注册渠道',
    `package` string comment '注册包来源',
    `register_product` string comment '注册产品',
    `register_type` int comment '注册类型',
    `register_result` int comment '注册结果',
    `register_result_reason` string comment '注册结果原因',
    `data_source` string comment '数据来源',
    `create_time` string comment '创建时间'
) partitioned by (`dt` string )
row format delimited fields terminated by '\t'
LINES TERMINATED BY '\n';

//日分区插入
insert overwrite table sinaif_commerce_dm.mid_register_events PARTITION(dt='20190401')
select phone,deviceid,userid as accountid,createtime as register_time,
       channelid as register_channel,NULL as package,"1003" as register_product,
       NULL as register_type,1 as register_result,NULL as register_result_reason,
       "0" as data_source,createtime as create_time
from sinaif_easy.t_device_sync where dt='20190401'
union
select username as phone,deviceid,id as accountid,
        registtime as register_time,
		NULL as register_channel,
        channelid as package,
        "1003" as register_product,
         registtype as register_type,
         status as register_result,
         remark as register_result_reason,
         "1" as data_source,createtime as create_time
from sinaif_easy.t_user_account where dt='20190401'
