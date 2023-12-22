#!/usr/bin/env python3
from zhdate import ZhDate
import datetime
print('国庆假期预测器\n键入"help"查看帮助')
holidayFirst = endDate = lieuDate1 = lieuDate2 = 0
userInputList = []
def fcnd():
    fcYear = int(userInputList[1])
    # ma代表Mid-Autumn Festival , 即中秋节, 下同
    maDate = ZhDate(fcYear, 8, 15).to_datetime()
    ndDate = datetime.datetime(fcYear, 10, 1) # nd代表National Day, 即国庆节, 下同
    maDoW = maDate.weekday()  # DoW, 即DateOfWeek, 下同
    ndDoW = ndDate.weekday()#unused --IAmREGE
    maInNd = 0
    if maDoW >= 4 and datetime.timedelta(days=-3) <= maDate - ndDate <=\
                    datetime.timedelta(days=0):
        holidayFirst = maDate  # holidayFirst, 即假期的第一天, 下同
        maInNd = 1
    if maDate == ndDate:
        holidayFirst = maDate
        maInNd = 1
    if datetime.timedelta(days=0) < maDate - ndDate <= \
        datetime.timedelta(days=7):
        holidayFirst = ndDate
        maInNd = 1
    holidayDays = 7 + maInNd  # holidayDays, 即假期天数, 下同
    if not maInNd:
        holidayFirst = ndDate
    holidayFirstDoW = holidayFirst.weekday()
    endDate = holidayFirst + datetime.timedelta(days=holidayDays-1, hours=23, minutes=59, seconds=59)
    endDoW = endDate.weekday()
    lieuDate1 = lieuDate2 = 'none' #lieu, 即调休, 下同
    if endDoW == 4:
        lieuDate1 = endDate + datetime.timedelta(seconds=1)
        lieuDate2 = endDate + datetime.timedelta(days=2)
    elif holidayFirstDoW == 0:
        lieuDate1 = holidayFirst - datetime.timedelta(days=2)
        lieuDate2 = holidayFirst - datetime.timedelta(seconds=1)
    elif holidayFirstDoW == 6 and holidayDays == 8:
        lieuDate1 = holidayFirst - datetime.timedelta(days=1)
    else:
        lieuDate1 = holidayFirst - datetime.timedelta(days=holidayFirstDoW+1)
        lieuDate2 = endDate + datetime.timedelta(days=5-endDoW)
    if lieuDate2 != 'none':
        return '国庆假期是'+str(holidayFirst)+' - '+str(endDate) , '调休时间为'+str(lieuDate1)+' / '+str(lieuDate2)
    else:
        return '国庆假期是'+str(holidayFirst)+' - '+str(endDate) , '调休时间为'+str(lieuDate1)
while True:
    runCommand = 0
    try:
        userInputList = input('>').lower().split(' ')
    except (KeyboardInterrupt, EOFError):
        break
    if userInputList[0] in ('forecast', 'fc'):
        try:
            if int(userInputList[1]) == 0:
                userInputList = ['fc', datetime.datetime.now().strftime("%Y")]
                print(fcnd())
            elif int(userInputList[1]) < 1949:
                print('醒醒, '+str(userInputList[1])+'年还没建国, 没有国庆节')
            else:
                print(fcnd())               
        except KeyboardInterrupt:
            break
        except:
            try:
                print('未知的参数' + str(userInputList[1]) + ', 键入"help"以获取帮助.')
            except IndexError:
                print('请输入要预测的年份!')
        runCommand = 1
    if userInputList[0] in ('fclist', 'forecastlist'):
        try:
            for i in range(int(userInputList[2]) - int(userInputList[1])+1):
                print(fcnd())
                userInputList = ['fc', int(userInputList[1])+1]
            runCommand = 1
        except KeyboardInterrupt:
            break
        except:
            try:
                print('未知的参数' + str(userInputList[1], userInputList[2]) + ', 键入"help"以获取帮助.')
            except IndexError:
                print('请输入要预测的年份!')
    if userInputList[0] == 'help':
        print('帮助信息：\n输入"forecast"(可简写为fc) + 年份 即可预测那一年的国庆假期.\n输入"quit"或"exit"可以退出程序\n输入"forecastlist"(可简写为fclist) + 第一年年份 + 最后一年年份可获得此区间内的国庆假期的安排')
        runCommand = 1
    if userInputList[0] in ('exit', 'quit'):
        break
    if not runCommand:
        print('未知的参数' + str(userInputList) + ', 键入"help"以获取帮助.')
