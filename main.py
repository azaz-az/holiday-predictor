from zhdate import ZhDate
import datetime
print('国庆假期预测器')
print('键入\"help\"查看帮助')
while True:
    runnedCommand = 0
    userInput = input('>')
    userInput = ' ' + str(userInput)
    userInputList = []
    j = -1
    for i in range(len(userInput)):
        j = j + 1
        if str(userInput[j]) == ' ':
            userInputList.append('')
        else:
            userInputList[-1] = str(userInputList[-1]) + str(userInput[j])
    if userInputList[0] == 'forecast' or userInputList[0] == 'fc':
        try:
            fcYear = int(userInputList[1])
            # ma代表Mid-Autumn Festival , 即中秋节，下同
            maDate = ZhDate(fcYear, 8, 15).to_datetime()
            ndDate = datetime.datetime(fcYear, 10, 1)  # nd代表National Day，即国庆节，下同
            maDoW = maDate.weekday()  # DoW, 即DateOfWeek，下同
            ndDoW = ndDate.weekday()
            maInNd = 0
            if maDoW == 4 and maDate - ndDate <= datetime.timedelta(days=0) and maDate - ndDate >= datetime.timedelta(days=-3):
                holidayFirst = maDate  # holidayFirst，即假期的第一天，下同
                holidayDays = 8  # holidayDays，即假期天数，下同
                maInNd = 1
            if maDate == ndDate:
                holidayFirst = maDate
                holidayDays = 8
                maInNd = 1
            if maDate - ndDate > datetime.timedelta(days=0) and maDate - ndDate <= datetime.timedelta(days=7):
                holidayFirst = ndDate
                holidayDays = 8
                maInNd = 1
            if maInNd == 0:
                holidayFirst = ndDate
                holidayDays = 7
            holidayFirstDoW = holidayFirst.weekday()
            endDate = holidayFirst + datetime.timedelta(days=holidayDays-1, hours=23, minutes=59, seconds=59)
            endDoW = endDate.weekday()
            lieuDate1 = 'none'
            lieuDate2 = 'none'
            if endDoW == 4:
                lieuDate1 = endDate + datetime.timedelta(seconds=1) #lieu，即调休，下同
                lieuDate2 = endDate + datetime.timedelta(days=2)
            else:
                if holidayFirstDoW == 0:
                    lieuDate1 = holidayFirst - datetime.timedelta(days=2)
                    lieuDate2 = holidayFirst - datetime.timedelta(seconds=1)
                else:
                    if holidayFirstDoW == 6 and holidayDays == 8:
                        lieuDate1 = holidayFirst - datetime.timedelta(days=1)
                    else:
                        lieuDate1 = holidayFirst - datetime.timedelta(days=holidayFirstDoW+1)
                        lieuDate2 = endDate + datetime.timedelta(days=5-endDoW)

            if int(userInputList[1]) < 1949:
                print('醒醒, '+str(userInputList[1])+'年还没建国, 没有国庆节')
            else:
                print('国庆假期是'+str(holidayFirst)+' - '+str(endDate))
                if lieuDate2 != 'none':
                    print('调休时间为'+str(lieuDate1)+' / '+str(lieuDate2))
                else:
                    print('调休时间为'+str(lieuDate1))
        except:
            try:
                print('未知的参数' + str(userInputList[1]) + ', 键入\"help\"以获取帮助.')
            except:
                print('请输入要预测的年份!')
        runnedCommand = 1
    if userInputList[0] == 'help':
        print('帮助信息：\n输入\"forecast\"(可简写为fc) + 年份 即可预测那一年的国庆假期.')
        runnedCommand = 1
    if runnedCommand == 0:
        print('未知的参数' + str(userInputList) + ', 键入\"help\"以获取帮助.')
