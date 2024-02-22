"""
Holiday Predictor / 假期预测器 - 基于 Python 的调休预测工具。

Copyright (C) 2024

原作 azaz-az。由 NebuDr1ft 派生并修改。

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

from data import Data


def calculation(given_list: list[str]) -> str:
    """该函数用于计算假期日期和调休日期。

    该函数计算指定的年份中，用户输入的假期的日期和这个假期的调休情况。

    Args:
        given_list (list[str]): 传入用户的输入，这是以用空格拆分后的列表形式输入的。

    Returns:
        str: 返回需要打印的输出字符串。
    """

    # 下述代码从传入参数中获取必要信息。
    forecast_year: int = int(given_list[1])
    holiday_name: str = str(given_list[2])
    hld_startdate = "None"  # Pylance: reportPossiblyUnboundVariable
    hld_enddate = "None"  # Pylance: reportPossiblyUnboundVariable

    # 这两个变量定义调休的日期。在随后会被修改，用 "None" 来判定是否有调休出现。
    lieu_1 = lieu_2 = "None"

    if holiday_name == "--national-day" or holiday_name == "-nd":  # 该部分用于处理国庆假期的调休预测。
        if forecast_year < 1949:
            return "错误的输入。给定年份 " + str(forecast_year) + " 不存在国庆假期。"
        else:
            # 下述代码对中秋节、国庆节的日期进行运算。
            mid_date = ZhDate(
                forecast_year, 8, 15
            ).to_datetime()  # 该变量是中秋节的日期。
            nati_date = datetime.datetime(
                forecast_year, 10, 1
            )  # 该变量是国庆节开始的日期。
            mid_dateofweek = mid_date.weekday()  # 该变量表明中秋节在周几。
            # national_day_date_of_week = national_day_date.weekday()
            is_mid_in_nati: bool = (
                False  # 该变量用于确定中秋节是否与国庆节相连或被包含其中。
            )
            hld_startdate = nati_date  # Pylance: reportPossiblyUnboundVariable

            # 下述代码对假期开始的日期进行运算。
            if (
                mid_dateofweek >= 4
                and datetime.timedelta(days=-3)
                <= mid_date - nati_date
                <= datetime.timedelta(days=0)
            ) or (mid_date == nati_date):
                hld_startdate = mid_date
                is_mid_in_nati = True
            if (
                datetime.timedelta(days=0)
                < mid_date - nati_date
                <= datetime.timedelta(days=7)
            ):
                hld_startdate = nati_date
                is_mid_in_nati = True
            if not is_mid_in_nati:
                hld_startdate = nati_date

            # 下述代码对假期结束的日期进行运算。
            hld_days = 7 + is_mid_in_nati  # 该变量指示了假期的长度。
            hld_start_dateofweek = hld_startdate.weekday()  # 该变量表明假期在周几开始。
            hld_enddate = hld_startdate + datetime.timedelta(
                days=hld_days - 1, hours=23, minutes=59, seconds=59
            )  # 该变量是假期结束的日期。
            hld_end_dateofweek = hld_enddate.weekday()  # 该变量表明假期在周几结束。

            # 下述代码对调休的日期进行运算。
            if hld_end_dateofweek == 4:
                lieu_1 = hld_enddate + datetime.timedelta(seconds=1)
                lieu_2 = hld_enddate + datetime.timedelta(days=2)
            elif hld_start_dateofweek == 0:
                lieu_1 = hld_startdate - datetime.timedelta(days=2)
                lieu_2 = hld_startdate - datetime.timedelta(seconds=1)
            elif hld_start_dateofweek == 6 and hld_days == 8:
                lieu_1 = hld_startdate - datetime.timedelta(days=1)
            else:
                lieu_1 = hld_startdate - datetime.timedelta(
                    days=hld_start_dateofweek + 1
                )
                lieu_2 = hld_enddate + datetime.timedelta(days=5 - hld_end_dateofweek)

    if holiday_name == "--new-year" or holiday_name == "-ny":  # 该部分用于处理元旦假期的调休预测。
        new_year_date = datetime.datetime(year=forecast_year, month=1, day=1)
        new_year_dateofweek = new_year_date.weekday()

        hld_startdate = "None"
        hld_enddate = "None"
        # 下述代码对元旦假期的调休进行运算。
        if new_year_dateofweek == 0:
            # 不调休
            hld_days = 3
            hld_startdate = datetime.datetime(year=forecast_year - 1, month=12, day=30)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=1, hour=23, minute=59, second=59
            )
        if new_year_dateofweek == 1:
            # 调休
            hld_days = 3
            hld_startdate = datetime.datetime(year=forecast_year - 1, month=12, day=30)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=1, hour=23, minute=59, second=59
            )
            lieu_1 = datetime.datetime(year=forecast_year - 1, month=12, day=29)
        if new_year_dateofweek == 2:
            # 不调休
            hld_days = 1
            hld_startdate = datetime.datetime(year=forecast_year, month=1, day=1)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=1, hour=23, minute=59, second=59
            )
        if new_year_dateofweek == 3:
            # 调休
            hld_days = 3
            hld_startdate = datetime.datetime(year=forecast_year, month=1, day=1)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=1, hour=23, minute=59, second=59
            )
            lieu_1 = datetime.datetime(year=forecast_year, month=1, day=4)
        if new_year_dateofweek == 4:
            # 不调休
            hld_days = 3
            hld_startdate = datetime.datetime(year=forecast_year, month=1, day=1)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=3, hour=23, minute=59, second=59
            )
        if new_year_dateofweek == 5:
            # 不调休
            hld_days = 3
            hld_startdate = datetime.datetime(year=forecast_year, month=1, day=1)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=3, hour=23, minute=59, second=59
            )
        if new_year_dateofweek == 6:
            # 不调休
            hld_days = 3
            hld_startdate = datetime.datetime(year=forecast_year - 1, month=12, day=31)
            hld_enddate = datetime.datetime(
                year=forecast_year, month=1, day=2, hour=23, minute=59, second=59
            )

    if lieu_1 != "None" and lieu_2 != "None":
        return (
            "假期由 "
            + str(hld_startdate)
            + " 起，直到 "
            + str(hld_enddate)
            + "。调休时间为 "
            + str(lieu_1.date())
            + " 和 "
            + str(lieu_2.date())
            + "。"
        )
    elif lieu_1 != "None":
        return (
            "假期由 "
            + str(hld_startdate)
            + " 起，直到 "
            + str(hld_enddate)
            + "。调休时间为 "
            + str(lieu_1.date())
            + "。"
        )
    else:
        return "假期由 " + str(hld_startdate) + " 起，直到 " + str(hld_enddate) + "。"

if __name__ == "__main__":
    print("Holiday Predictor / 假期预测器 - 基于 Python 的调休预测工具")
    print("键入 help 以查看帮助。")

    LIEU_DATE_1 = LIEU_DATE_2 = 0
    input_list: list[str] = []  # 初始化 input_list

    while True:
        execution_flag: bool = (
            False  # 该变量用于报告用户输入是否命中某个指令。在下面的代码中，用户输入触发对任意指令的处理后，该变量即被设置为 True。
        )

        try:  # 这段代码判定是否让程序进入调试模式。调试模式默认处于关闭状态。
            input_list = input("> ").lower().split(" ")
        except (KeyboardInterrupt, EOFError):
            print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。\n")
            break

        if input_list[0] in ("forecast", "fc"):  # 处理用户发起的 forecast 指令请求。
            try:
                print(calculation(input_list))
            except (KeyboardInterrupt, EOFError):
                print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。")
                break
            except Exception as e:  # pylint: disable = W0702, W0718
                print("程序未按预期进行。\n\n可能的原因：")
                if len(input_list) <= 2:
                    print("可能缺少了指令、年份 和/或 参数。")
                elif (input_list[2])[0] == "-" and (input_list[2])[1] != "-":
                    print(f'输入的参数有误。你想输入 "-{input_list[2]}" 吗？')
                else:
                    print("程序无法定位错误的原因。可能是参数输入错误，也有可能是程序运行错误。")
                print(f"抛出了异常 {e}。")
                print('\n如果你不会使用该程序，键入 "help" 以查看帮助。')
                print(
                    "如果无法定位程序未按预期运行的原因，请向我们报告错误。https://github.com/azaz-az/holiday-predictor\n"
                )
            execution_flag = True  # pylint: disable = C0103

        if input_list[0] == "help":
            print(Data.help)
            execution_flag = True # pylint: disable = C0103

        if input_list[0] in ("exit", "quit"):
            break

        if not execution_flag:
            print("未知的指令 " + str(input_list[0]) + '。键入 "help" 以查看帮助。')