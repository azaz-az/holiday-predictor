"""
Holiday Predictor / 假期预测器 - 基于 Python 的调休预测工具。

Copyright (C) 2024

原作 azaz-az，由 NebuDr1ft 派生并修改。

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime

from zhdate import ZhDate  # type: ignore

from config import Config
from data import Data


def calculation(given_list: list[str]):
    forecast_year: int = int(given_list[1])
    holiday_name: str = str(given_list[2])
    lieu_date_1 = lieu_date_2 = 'none'  # lieu, 即调休, 下同

    if holiday_name == '--national':  # 该部分用于处理国庆假期的调休预测
        if forecast_year < 1949:
            print(f"错误的输入。给定年份 {forecast_year} 不存在国庆假期。")
        else:
            mid_autumn_date = ZhDate(forecast_year, 8, 15).to_datetime()
            national_day_date = datetime.datetime(forecast_year, 10, 1)
            mid_autumn_date_of_week = mid_autumn_date.weekday()
            # national_day_date_of_week = national_day_date.weekday()
            is_mid_autumn_in_national_day: bool = False  # 该变量用于确定中秋节是否与国庆节相连。
            holiday_start_date = national_day_date  # 注意：该行不对变量的终值进行任何修改，仅为解决 Pylance 的 reportPossiblyUnboundVariable 问题
            if (mid_autumn_date_of_week >= 4 and datetime.timedelta(days=-3) <= mid_autumn_date - national_day_date <= datetime.timedelta(days=0)) or (mid_autumn_date == national_day_date):
                holiday_start_date = mid_autumn_date
                is_mid_autumn_in_national_day = True
            if datetime.timedelta(days=0) < mid_autumn_date - national_day_date <= datetime.timedelta(days=7):
                holiday_start_date = national_day_date
                is_mid_autumn_in_national_day = True
            if not is_mid_autumn_in_national_day:
                holiday_start_date = national_day_date
            holiday_days = 7 + is_mid_autumn_in_national_day  # 该变量指示了假期的长度。
            holiday_first_date_of_week = holiday_start_date.weekday()
            holiday_end_date = holiday_start_date + datetime.timedelta(days=holiday_days - 1, hours=23, minutes=59, seconds=59)
            holiday_end_date_of_week = holiday_end_date.weekday()
            if holiday_end_date_of_week == 4:
                lieu_date_1 = holiday_end_date + datetime.timedelta(seconds=1)
                lieu_date_2 = holiday_end_date + datetime.timedelta(days=2)
            elif holiday_first_date_of_week == 0:
                lieu_date_1 = holiday_start_date - datetime.timedelta(days=2)
                lieu_date_2 = holiday_start_date - datetime.timedelta(seconds=1)
            elif holiday_first_date_of_week == 6 and holiday_days == 8:
                lieu_date_1 = holiday_start_date - datetime.timedelta(days=1)
            else:
                lieu_date_1 = holiday_start_date - datetime.timedelta(days=holiday_first_date_of_week + 1)
                lieu_date_2 = holiday_end_date + datetime.timedelta(days=5 - holiday_end_date_of_week)

    if input_list[2] == '--newyear':  # 该部分用于处理元旦假期的调休预测
        new_year_date = datetime.datetime(year=forecast_year, month=1, day=1)
        new_year_dow = new_year_date.weekday()
        if new_year_dow == 6:
            # 不调休
            holiday_days = 3
            holiday_start_date = datetime.datetime(year=forecast_year-1, month=12, day=31)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=2, hour=23, minute=59, second=59)
        if new_year_dow == 0:
            # 不调休
            holiday_days = 3
            holiday_start_date = datetime.datetime(year=forecast_year-1, month=12, day=30)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
        if new_year_dow == 1:
            # 调休
            holiday_days = 3
            holiday_start_date = datetime.datetime(year=forecast_year-1, month=12, day=30)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
            lieu_date_1 = datetime.datetime(year=forecast_year-1, month=12, day=29)
        if new_year_dow == 2:
            # 不调休
            holiday_days = 1
            holiday_start_date = datetime.datetime(year=forecast_year, month=1, day=1)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
        if new_year_dow == 3:
            # 调休
            holiday_days = 3
            holiday_start_date = datetime.datetime(year=forecast_year, month=1, day=1)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=1, hour=23, minute=59, second=59)
            lieu_date_1 = datetime.datetime(year=forecast_year, month=1, day=4)
        if new_year_dow == 4:
            # 不调休
            holiday_days = 3
            holiday_start_date = datetime.datetime(year=forecast_year, month=1, day=1)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=3, hours=23, minutes=59, seconds=59)
        if new_year_date == 5:
            # 不调休
            holiday_days = 3
            holiday_start_date = datetime.datetime(year=forecast_year, month=1, day=1)
            holiday_end_date = datetime.datetime(year=forecast_year, month=1, day=3, hours=23, minutes=59, seconds=59)
        if Config.debug_mode:
            print('holiday_days=', holiday_days)
            print('holiday_first=', holiday_start_date)
            print('new_year_dow=', new_year_dow)
            print('end_date=', holiday_end_date)
            print('---Debug Info End---')  # TODO: 使用更优雅的 Debug 输出方式
    if lieu_date_2 != 'none':
        return '假期是' + str(holiday_start_date) + ' - ' + str(holiday_end_date), '调休时间为' + str(lieu_date_1) + ' / ' + str(
            lieu_date_2)
    elif lieu_date_1 != 'none':
        return '假期是' + str(holiday_start_date) + ' - ' + str(holiday_end_date), '调休时间为' + str(lieu_date_1)
    else:
        return '假期是' + str(holiday_start_date) + ' - ' + str(holiday_end_date)


if __name__=="__main__":
    print("Holiday Predictor / 假期预测器 - 基于 Python 的调休预测工具")
    print("键入 help 以查看帮助。")

    holiday_first = end_date = lieu_date_1 = lieu_date_2 = 0
    input_list: list[str] = []  # 初始化 input_list

    while True:
        execution_flag: bool = False  # 该变量用于报告用户输入是否命中某个指令。在下面的代码中，用户输入触发对任意指令的处理后，该变量即被设置为 True。

        try:  # 这段代码判定是否让程序进入调试模式。调试模式默认处于关闭状态。
            input_list = input('> ').lower().split(' ')
        except (KeyboardInterrupt, EOFError):
            print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。\n")
            break

        if input_list[0] in ('forecast', 'fc'):  # 处理用户发起的 forecast 指令请求。
            try:
                print(calculation(input_list))
            except (KeyboardInterrupt, EOFError):
                print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。")
                break
            except:  # pylint: disable=W0702
                print("程序未按预期进行。\n\n可能的原因：")
                if len(input_list) <= 2:
                    print('输入的参数有误。')
                elif (input_list[2])[0] == '-' and (input_list[2])[1] != '-':
                    print(f'输入的参数有误。你想输入 "-{input_list[2]}" 吗？')
                else:
                    print('程序无法定位错误的原因。')
                print('\n键入 "help" 以查看帮助。')
                print('如果无法定位程序未按预期运行的原因，请向我们报告错误。https://github.com/NebuDr1ft/holiday-predictor\n')
            execution_flag = True

        if input_list[0] == 'help':
            print(Data.help)
            execution_flag = True

        if input_list[0] in ('exit', 'quit'):
            break

        if not execution_flag:
            print("未知的指令 " + str(input_list[0]) + "。键入 \"help\" 以查看帮助。")

        if Config.debug_mode == execution_flag == True:
            break
