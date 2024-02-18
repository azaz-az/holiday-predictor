#!/usr/bin/env python3
from zhdate import ZhDate
import datetime

debug_mode = 0
print('假期预测器\n键入"help"查看帮助')
holiday_first = end_date = lieu_date_1 = lieu_date_2 = 0
user_input_list = []

def forecast_chl(holiday_name):
    forecast_year = int(user_input_list[1])
    lieu_date_1 = lieu_date_2 = 'none'  # lieu, 即调休, 下同
    if holiday_name == '--national':
        # ma代表Mid-Autumn Festival , 即中秋节, 下同
        mid_autumn_date = ZhDate(forecast_year, 8, 15).to_datetime()
        national_day_date = datetime.datetime(forecast_year, 10, 1)  # nd代表National Day, 即国庆节, 下同
        mid_autumn_dow = mid_autumn_date.weekday()  # DoW, 即DateOfWeek, 下同
        national_day_dow = national_day_date.weekday()
        mid_autumn_in_national_day = 0  # maInNd 即中秋节包含在国庆节内，0代表False，1代表True，下同
    if holiday_name == '--newyear':
        new_year_date = datetime.datetime(year=forecast_year, month=1, day=1)
        new_year_dow = new_year_date.weekday()
    if holiday_name == '--national':
        if forecast_year < 1949:
            return('醒醒, ' + str(user_input_list[1]) + '年还没建国, 没有国庆节')
        if debug_mode == 1:
            print(user_input_list)
        if mid_autumn_dow >= 4 and datetime.timedelta(days=-3) <= mid_autumn_date - national_day_date <= \
                datetime.timedelta(days=0):
            holiday_first = mid_autumn_date  # holiday_first, 即假期的第一天, 下同
            mid_autumn_in_national_day = 1
        if mid_autumn_date == national_day_date:
            holiday_first = mid_autumn_date
            mid_autumn_in_national_day = 1
        if datetime.timedelta(days=0) < mid_autumn_date - national_day_date <= \
                datetime.timedelta(days=7):
            holiday_first = national_day_date
            mid_autumn_in_national_day = 1
        holiday_days = 7 + mid_autumn_in_national_day  # holiday_days, 即假期天数, 下同
        if not mid_autumn_in_national_day:
            holiday_first = national_day_date
        holiday_first_dow = holiday_first.weekday()
        end_date = holiday_first + datetime.timedelta(days=holiday_days - 1, hours=23, minutes=59, seconds=59)
        end_dow = end_date.weekday()
        if end_dow == 4:
            lieu_date_1 = end_date + datetime.timedelta(seconds=1)
            lieu_date_2 = end_date + datetime.timedelta(days=2)
        elif holiday_first_dow == 0:
            lieu_date_1 = holiday_first - datetime.timedelta(days=2)
            lieu_date_2 = holiday_first - datetime.timedelta(seconds=1)
        elif holiday_first_dow == 6 and holiday_days == 8:
            lieu_date_1 = holiday_first - datetime.timedelta(days=1)
        else:
            lieu_date_1 = holiday_first - datetime.timedelta(days=holiday_first_dow + 1)
            lieu_date_2 = end_date + datetime.timedelta(days=5 - end_dow)
    if holiday_name == '--newyear':
        if debug_mode == 1:
            print('---Debug Info Start---')
            print('user_input_list: ', user_input_list)
        if new_year_dow == 6:
            # 不调休
            holiday_days = 3
            holiday_first = datetime.datetime(year=forecast_year-1, month=12, day=31)
            end_date = datetime.datetime(year=forecast_year, month=1, day=2, hour=23, minute=59, second=59)
        if new_year_dow == 0:
            # 不调休
            holiday_days = 3
            holiday_first = datetime.datetime(year=forecast_year-1, month=12, day=30)
            end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
        if new_year_dow == 1:
            # 调休
            holiday_days = 3
            holiday_first = datetime.datetime(year=forecast_year-1, month=12, day=30)
            end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
            lieu_date_1 = datetime.datetime(year=forecast_year-1, month=12, day=29)
        if new_year_dow == 2:
            # 不调休
            holiday_days = 1
            holiday_first = datetime.datetime(year=forecast_year, month=1, day=1)
            end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
        if new_year_dow == 3:
            # 调休
            holiday_days = 3
            holiday_first = datetime.datetime(year=forecast_year, month=1, day=1)
            end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
            lieu_date_1 = datetime.datetime(year=forecast_year, month=1, day=4)
        if new_year_dow == 4:
            # 不调休
            holiday_days = 3
            holiday_first = datetime.datetime(year=forecast_year, month=1, day=1)
            end_date = datetime.datetime(year=forecast_year, month=1, day=3, hours=23, minutes=59, seconds=59)
        if new_year_date == 5:
            # 不调休
            holiday_days = 3
            holiday_first = datetime.datetime(year=forecast_year, month=1, day=1)
            end_date = datetime.datetime(year=forecast_year, month=1, day=3, hours=23, minutes=59, seconds=59)
        if debug_mode == 1:
            print('holiday_days=', holiday_days)
            print('holiday_first=', holiday_first)
            print('new_year_dow=', new_year_dow)
            print('end_date=', end_date)
            print('---Debug Info End---')
    if lieu_date_2 != 'none':
        return '假期是' + str(holiday_first) + ' - ' + str(end_date), '调休时间为' + str(lieu_date_1) + ' / ' + str(
            lieu_date_2)
    elif lieu_date_1 != 'none':
        return '假期是' + str(holiday_first) + ' - ' + str(end_date), '调休时间为' + str(lieu_date_1)
    else:
        return '假期是' + str(holiday_first) + ' - ' + str(end_date)

if __name__ == '__main__':
    while True:
        run_command = 0
        try:
            if debug_mode != 1:
                user_input_list = input('>').lower().split(' ')
            else:
                user_input_list = str('fc 2023 --newyear').lower().split(' ')
        except (KeyboardInterrupt, EOFError):
            break
        if user_input_list[0] in ('forecast', 'fc'):
            try:
                if int(user_input_list[1]) == 0:
                    user_input_list = ['fc', datetime.datetime.now().strftime("%Y")]
                    print(forecast_chl(str(user_input_list[2])))
                else:
                    print(forecast_chl(str(user_input_list[2])))
            except KeyboardInterrupt:
                break
            except:
                try:
                    print('未知的参数, 键入"help"以获取帮助.\
                        \n\
                        \n快速分析(结果不一定准确):')
                    if len(user_input_list) <= 2:
                        print('你可能漏了句尾的选项')
                    elif (user_input_list[2])[0] == '-' and (user_input_list[2])[1] != '-':
                        print('选项值需要使用两条横线,而非一条')
                    else:
                        print('暂无可用的快速修复.')
                    print('若按照快速分析的方法进行后仍无法解决,请键入help获得更详细的帮助\
                        \n如果依然无法解决,请前往本项目的GitHub页面(https://github.com/azaz-az/holiday-predictor)给我提issue.\n')
                except IndexError:
                    print('请输入要预测的年份!')
            run_command = 1  # 标记代码已被运行，接下来就不会输出未找到命令
        if user_input_list[0] in ('fclist', 'forecastlist'):
            try:
                for i in range(int(user_input_list[2]) - int(user_input_list[1]) + 1):
                    print(forecast_chl(str(user_input_list[2])))
                    user_input_list = ['fc', int(user_input_list[1]) + 1]
                run_command = 1
            except KeyboardInterrupt:
                break
            except:
                try:
                    print('未知的参数' + str(user_input_list[1], user_input_list[2]) + ', 键入"help"以获取帮助.')
                except IndexError:
                    print('请输入要预测的年份!')
        if user_input_list[0] == 'help':
            print('帮助信息：\n输入"forecast(可简写为fc) + <年份> + <选项>"即可预测那一年的假期.\
                \n输入"quit"或"exit"可以退出程序\
                \n输入"forecastlist"(可简写为fclist) + 第一年年份 + 最后一年年份可获得此区间内的国庆假期\
                \n(注意:fclist功能暂时只支持预测国庆假期,不支持预测其他假期的安排，后续可能会更新)\
                \n\
                \n<选项>允许的参数值有：\
                \n--national: 预测国庆假期\
                \n--newyear: 预测元旦假期\
                \n特别注意:选项需要两条横线，而非一条横线')
            run_command = 1
        if user_input_list[0] in ('exit', 'quit'):
            break
        if not run_command:
            print('未知的参数' + str(user_input_list) + ', 键入"help"以获取帮助.')
        if debug_mode == run_command == 1:
            break
