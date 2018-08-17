import itchat
import pandas as pd
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)
number_of_friends = len(friends)
df_friends = pd.DataFrame(friends)
print(number_of_friends)
print(df_friends)
path=input('请输入你要保存的路径')#切记为.xls格式
df_friends.to_excel(path)