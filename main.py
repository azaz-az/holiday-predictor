"""预测中国的假期安排的模块。
前置模块：zhdate
用法：CalculationUtil.假期名(年份)
输出：<假期开始日期>, <假期结束日期>, [调休日期1(若有)], [调休日期2(若有)]
"""

"""
Holiday Predictor / 假期预测器 - 基于 Python 的调休预测工具。

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

__all__ = ["CalculationUtil", "calculation"]

import sys

from typing import List, Optional, Tuple

import datetime

from zhdate import ZhDate  # type: ignore

from data import Data


class CalculationUtil:
    """计算假期安排所需的类。
    用法：CalculationUtil.假期名(年份)
    输出：<假期开始日期>, <假期结束日期>, [调休日期1(若有)], [调休日期2(若有)]
    """

    @staticmethod
    def national_day(year: int) -> Optional[Tuple[
        datetime.datetime, datetime.datetime, Optional[datetime.datetime],
        Optional[datetime.datetime]
    ]]:
        if year < 1949:
            return None
        # 下述代码从传入参数中获取必要信息。

        # 这两个变量定义调休的日期。在随后会被修改，用 "None" 来判定是否有调休出现。
        lieu_2: Optional[datetime.datetime] = None
        # 下述代码对中秋节、国庆节的日期进行运算。
        mid_date: datetime.datetime = ZhDate(
            year, 8, 15
        ).to_datetime()  # 该变量是中秋节的日期。
        nati_date = datetime.datetime(
            year, 10, 1
        )  # 该变量是国庆节开始的日期。
        mid_dateofweek: int = mid_date.weekday()  # 该变量表明中秋节在周几。
        # national_day_date_of_week = national_day_date.weekday()
        is_mid_in_nati: bool = \
            False  # 该变量用于确定中秋节是否与国庆节相连或被包含其中。
        hld_startdate: datetime.datetime = nati_date

        # 下述代码对假期开始的日期进行运算。
        if (
                mid_dateofweek >= 4
                and datetime.timedelta(days=-3)
                <= mid_date - nati_date
                <= datetime.timedelta(days=0)
        ) or (mid_date == nati_date):
            hld_startdate = mid_date
            is_mid_in_nati = True
        if datetime.timedelta(days=0) \
                < mid_date - nati_date \
                <= datetime.timedelta(days=7):
            hld_startdate = nati_date
            is_mid_in_nati = True
        if not is_mid_in_nati:
            hld_startdate = nati_date

        # 下述代码对假期结束的日期进行运算。
        hld_days: int = 7 + is_mid_in_nati  # 该变量指示了假期的长度。
        hld_start_dateofweek: int = hld_startdate.weekday()  # 该变量表明假期在周几开始。
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
        return hld_startdate, hld_enddate, lieu_1, lieu_2

    @staticmethod
    def new_year(year: int) -> Tuple[
        datetime.datetime, datetime.datetime, Optional[datetime.datetime]
    ]:
        new_year_date: datetime.datetime = datetime.datetime(
            year=year, month=1, day=1
        )
        new_year_dateofweek: int = new_year_date.weekday()
        hld_startdate: datetime.datetime = \
            new_year_date + datetime.timedelta(
                Data.HLD_3DAYS_START_DELTA_DAY[new_year_dateofweek]
            )

        hld_enddate: datetime.datetime = \
            new_year_date + datetime.timedelta(
                Data.HLD_3DAYS_END_DELTA_DAY[new_year_dateofweek]
            )

        lieu_1: Optional[datetime.datetime] = \
            new_year_date + datetime.timedelta(
                Data.HLD_3DAYS_LIEU1_DELTA_DAY[new_year_dateofweek]  # type: ignore
            ) if Data.HLD_3DAYS_LIEU1_DELTA_DAY[new_year_dateofweek] is not None \
                else None  # type: ignore
        return hld_startdate, hld_enddate, lieu_1

    @staticmethod
    def spring_festival(year: int) -> Tuple[
        datetime.datetime, datetime.datetime, datetime.datetime,
        datetime.datetime
    ]:
        spring_festival_date: datetime.datetime = \
            ZhDate(year, 1, 1).to_datetime()
        spring_festival_dateofweek: int = spring_festival_date.weekday()
        # 下述代码对春节假期的调休进行运算。
        hld_startdate: datetime.datetime = \
            spring_festival_date + datetime.timedelta(
                Data.SPRING_FESTIVAL_START_DELTA_DAY[spring_festival_dateofweek]
            )
        hld_enddate: datetime.datetime = \
            spring_festival_date + datetime.timedelta(
                Data.SPRING_FESTIVAL_END_DELTA_DAY[spring_festival_dateofweek]
            )
        lieu_1: datetime.datetime = \
            spring_festival_date + datetime.timedelta(
                Data.SPRING_FESTIVAL_LIEU1_DELTA_DAY[spring_festival_dateofweek]
            )
        lieu_2: datetime.datetime = \
            spring_festival_date + datetime.timedelta(
                Data.SPRING_FESTIVAL_LIEU2_DELTA_DAY[spring_festival_dateofweek]
            )
        return hld_startdate, hld_enddate, lieu_1, lieu_2

    @staticmethod
    def qing_ming(year: int) -> Tuple[
        datetime.datetime, datetime.datetime, Optional[datetime.datetime]
    ]:
        qing_ming_date: datetime.datetime = datetime.datetime(
            year=year, month=4,
            day=5 if year % 4 or (year % 400 and not year % 100) else 4
        )
        qing_ming_dateofweek: int = qing_ming_date.weekday()
        # 下述代码对清明假期的调休进行运算。
        hld_startdate: datetime.datetime = \
            qing_ming_date + datetime.timedelta(
                Data.HLD_3DAYS_START_DELTA_DAY[qing_ming_dateofweek]
            )

        hld_enddate: datetime.datetime = \
            qing_ming_date + datetime.timedelta(
                Data.HLD_3DAYS_END_DELTA_DAY[qing_ming_dateofweek]
            )

        lieu_1: Optional[datetime.datetime] = \
            qing_ming_date + datetime.timedelta(
                Data.HLD_3DAYS_LIEU1_DELTA_DAY[qing_ming_dateofweek]  # type: ignore
            ) if Data.HLD_3DAYS_LIEU1_DELTA_DAY[qing_ming_dateofweek] is not None \
                else None  # type: ignore
        return hld_startdate, hld_enddate, lieu_1

    @staticmethod
    def duan_wu(year: int) -> Tuple[
        datetime.datetime, datetime.datetime, Optional[datetime.datetime]
    ]:
        duan_wu_date: datetime.datetime = ZhDate(year, 5, 5).to_datetime()
        duan_wu_dateofweek: int = duan_wu_date.weekday()
        # 下述代码对端午假期的调休进行运算。
        hld_startdate: datetime.datetime = \
            duan_wu_date + datetime.timedelta(
                Data.HLD_3DAYS_START_DELTA_DAY[duan_wu_dateofweek]
            )

        hld_enddate: datetime.datetime = \
            duan_wu_date + datetime.timedelta(
                Data.HLD_3DAYS_END_DELTA_DAY[duan_wu_dateofweek]
            )

        lieu_1: Optional[datetime.datetime] = \
            duan_wu_date + datetime.timedelta(
                Data.HLD_3DAYS_LIEU1_DELTA_DAY[duan_wu_dateofweek]  # type: ignore
            ) if Data.HLD_3DAYS_LIEU1_DELTA_DAY[duan_wu_dateofweek] is not None \
                else None  # type: ignore
        return hld_startdate, hld_enddate, lieu_1

    @staticmethod
    def international_labours_day(year: int) -> Optional[Tuple[
        datetime.datetime, datetime.datetime, datetime.datetime,
        datetime.datetime
    ]]:
        if year < 1890:
            return None
        international_labours_day_date: datetime.datetime = \
            datetime.datetime(year=year, month=5, day=1)
        international_labours_day_dateofweek: int = \
            international_labours_day_date.weekday()
        # 下述代码对五一假期的调休进行运算。
        hld_startdate: datetime.datetime = \
            international_labours_day_date + datetime.timedelta(
                Data.INTERNATIONAL_LABOURS_DAY_START_DELTA_DAY[
                    international_labours_day_dateofweek
                ]
            )
        hld_enddate: datetime.datetime = \
            international_labours_day_date + datetime.timedelta(
                Data.INTERNATIONAL_LABOURS_DAY_END_DELTA_DAY[
                    international_labours_day_dateofweek
                ]
            )
        lieu_1: datetime.datetime = \
            international_labours_day_date + datetime.timedelta(
                Data.INTERNATIONAL_LABOURS_DAY_LIEU1_DELTA_DAY[
                    international_labours_day_dateofweek
                ]
            )
        lieu_2: datetime.datetime = \
            international_labours_day_date + datetime.timedelta(
                Data.INTERNATIONAL_LABOURS_DAY_LIEU2_DELTA_DAY[
                    international_labours_day_dateofweek
                ]
            )
        return hld_startdate, hld_enddate, lieu_1, lieu_2

    @classmethod
    def mid_autumn(cls, year: int) -> Tuple[
        datetime.datetime, datetime.datetime, Optional[datetime.datetime],
        Optional[datetime.datetime]
    ]:
        mid_autumn_date: datetime.datetime = \
            ZhDate(year, 8, 15).to_datetime()
        mid_autumn_dateofweek: int = mid_autumn_date.weekday()
        # 下述代码对中秋假期的调休进行运算。
        if year >= 1949:
            national_day_result: Optional[Tuple[
                datetime.datetime, datetime.datetime,
                Optional[datetime.datetime], Optional[datetime.datetime]
            ]] = cls.national_day(year)
            if national_day_result is not None and \
                    (national_day_result[1] - national_day_result[0]).days > 6:
                return national_day_result
        hld_startdate: datetime.datetime = \
            mid_autumn_date + datetime.timedelta(
                Data.HLD_3DAYS_START_DELTA_DAY[mid_autumn_dateofweek]
            )

        hld_enddate: datetime.datetime = \
            mid_autumn_date + datetime.timedelta(
                Data.HLD_3DAYS_END_DELTA_DAY[mid_autumn_dateofweek]
            )

        lieu_1: Optional[datetime.datetime] = \
            mid_autumn_date + datetime.timedelta(
                Data.HLD_3DAYS_LIEU1_DELTA_DAY[mid_autumn_dateofweek]  # type: ignore
            ) if Data.HLD_3DAYS_LIEU1_DELTA_DAY[mid_autumn_dateofweek] is not None \
                else None  # type: ignore
        return hld_startdate, hld_enddate, lieu_1, None


def calculation(given_list: List[str]) -> str:
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

    # 这两个变量定义调休的日期。在随后会被修改，用 "None" 来判定是否有调休出现。
    lieu_2: Optional[datetime.datetime] = None

    if holiday_name in ("--national-day", "-nd"):  # 该部分用于处理国庆假期的调休预测。
        national_day_result: Optional[Tuple[
            datetime.datetime, datetime.datetime, Optional[datetime.datetime],
            Optional[datetime.datetime]
        ]] = CalculationUtil.national_day(forecast_year)
        if national_day_result is None:
            return ("错误的输入。给定年份 {year} "
                    "不存在国庆假期。".format(year=forecast_year))
        hld_startdate, hld_enddate, lieu_1, lieu_2 = national_day_result
    elif holiday_name in ("--new-year", "-ny"):  # 该部分用于处理元旦假期的调休预测。
        hld_startdate, hld_enddate, lieu_1 = \
            CalculationUtil.new_year(forecast_year)
    elif holiday_name in ("--spring-festival", "-sf"):  # 该部分用于处理春节假期的调休预测。
        if '--do-not-output-notes' not in given_list:
            print(Data.spring_festival_note)
        spring_festival_result: Tuple[
            datetime.datetime, datetime.datetime, datetime.datetime,
            datetime.datetime
        ] = CalculationUtil.spring_festival(forecast_year)
        hld_startdate, hld_enddate, lieu_1, lieu_2 = spring_festival_result
    elif holiday_name in ("--qing-ming", "-qm"):  # 该部分用于处理清明假期的调休预测。
        hld_startdate, hld_enddate, lieu_1 = \
            CalculationUtil.qing_ming(forecast_year)
    elif holiday_name in ("--duan-wu", "-dw"):  # 该部分用于处理端午假期的调休预测。
        hld_startdate, hld_enddate, lieu_1 = \
            CalculationUtil.duan_wu(forecast_year)
    elif holiday_name in ("--international-labours-day", "-ild"):  # 该部分用于处理五一假期的调休预测。
        if '--do-not-output-notes' not in given_list:
            print(Data.international_labours_day_note)
        international_labours_day_result: Optional[Tuple[
            datetime.datetime, datetime.datetime, datetime.datetime,
            datetime.datetime
        ]] = CalculationUtil.international_labours_day(forecast_year)
        if international_labours_day_result is None:
            return ("错误的输入。给定年份 {year} "
                    "不存在五一假期。".format(year=forecast_year))
        hld_startdate, hld_enddate, lieu_1, lieu_2 = \
            international_labours_day_result
    elif holiday_name in ("--mid-autumn", "-ma"):  # 该部分用于处理中秋假期的调休预测。
        hld_startdate, hld_enddate, lieu_1, lieu_2 = \
            CalculationUtil.mid_autumn(forecast_year)
    else:
        return "不存在的参数 {name}。".format(name=holiday_name)
    hld_days: int = (hld_enddate - hld_startdate).days + 1
    if '--only-return-days' in given_list:
        return str(hld_days)
    if lieu_1 is not None and lieu_2 is not None:
        return ("假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。"
                "调休时间为 {lieu1}（星期{lieu1_dateofweek}）和 {lieu2}（星期{lieu2_dateofweek}）。".format(
            start=hld_startdate,
            start_dateofweek=Data.INT_TO_WEEKDAY[hld_startdate.weekday()],
            end=hld_enddate,
            end_dateofweek=Data.INT_TO_WEEKDAY[hld_enddate.weekday()],
            lieu1=lieu_1.date(),
            lieu1_dateofweek=Data.INT_TO_WEEKDAY[lieu_1.weekday()],
            lieu2=lieu_2.date(),
            lieu2_dateofweek=Data.INT_TO_WEEKDAY[lieu_2.weekday()],
            day=hld_days
        ))
    if lieu_1 is not None:
        return ("假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。"
                "调休时间为 {lieu}（星期{lieu_dateofweek}）。".format(
            start=hld_startdate,
            start_dateofweek=Data.INT_TO_WEEKDAY[hld_startdate.weekday()],
            end=hld_enddate,
            end_dateofweek=Data.INT_TO_WEEKDAY[hld_enddate.weekday()],
            lieu=lieu_1.date(),
            lieu_dateofweek=Data.INT_TO_WEEKDAY[lieu_1.weekday()],
            day=hld_days
        ))
    return "假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。".format(
        start=hld_startdate,
        start_dateofweek=Data.INT_TO_WEEKDAY[hld_startdate.weekday()],
        end=hld_enddate,
        end_dateofweek=Data.INT_TO_WEEKDAY[hld_enddate.weekday()],
        day=hld_days
    )


input_list: List[str]
if __name__ == "__main__" and len(sys.argv) < 2:
    print("\nHoliday Predictor / 假期预测器 - 基于 Python 的调休预测工具\n键入 help 以查看帮助。")

    LIEU_DATE_1 = LIEU_DATE_2 = 0
    input_list = []  # 初始化 input_list

    while True:
        execution_flag: bool = \
            False  # 该变量用于报告用户输入是否命中某个指令。在下面的代码中，用户输入触发对任意指令的处理后，该变量即被设置为 True。

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
                print("抛出了异常 {error!r}。".format(error=e))
                print('\n如果你不会使用该程序，键入 "help" 以查看帮助。')
                print("如果无法定位程序未按预期运行的原因，请向我们报告错误。"
                      "https://github.com/azaz-az/holiday-predictor\n")
            execution_flag = True  # pylint: disable = C0103

        if input_list[0] == "help":
            print(Data.help)
            execution_flag = True  # pylint: disable = C0103

        if input_list[0] in ("exit", "quit"):
            break

        if not execution_flag:
            print('未知的指令 {unknown}。'
                  '键入 "help" 以查看帮助。'.format(unknown=input_list[0]))
            print('\n如果你不会使用该程序，键入 "help" 以查看帮助。')
            print("如果无法定位程序未按预期运行的原因，请向我们报告错误。"
                  "https://github.com/azaz-az/holiday-predictor\n")
            execution_flag = True  # pylint: disable = C0103

elif __name__ == "__main__" and len(sys.argv) > 1:
    input_list = sys.argv[1:]

    if input_list[0] in ("forecast", "fc"):  # 处理用户发起的 forecast 指令请求。
        try:
            print(calculation(input_list))
            sys.exit(0)
        except Exception as e:  # pylint: disable = W0702, W0718
            print("程序未按预期进行。\n\n可能的原因：")
            if len(input_list) <= 2:
                print("可能缺少了指令、年份 和/或 参数。")
            elif (input_list[2])[0] == "-" and (input_list[2])[1] != "-":
                print(f'输入的参数有误。你想输入 "-{input_list[2]}" 吗？')
            else:
                print("程序无法定位错误的原因。可能是参数输入错误，也有可能是程序运行错误。")
            print("抛出了异常 {error!r}。".format(error=e))
            print('\n如果你不会使用该程序，键入 '
                  '"{arg0} help" 以查看帮助。'.format(arg0=sys.argv[0]))
            print("如果无法定位程序未按预期运行的原因，请向我们报告错误。"
                  "https://github.com/azaz-az/holiday-predictor\n")
            sys.exit(2)

    elif input_list[0] == "help":
        print(Data.help)
        sys.exit(0)

    else:
        print('未知的指令 {unknown}。'
              '键入 "{arg0} help" 以查看帮助。'.format(unknown=input_list[0],
                                                      arg0=sys.argv[0]))
        print('\n如果你不会使用该程序，键入 "{arg0} help" 以查看帮助。'.format(arg0=sys.argv[0]))
        print("如果无法定位程序未按预期运行的原因，请向我们报告错误。"
              "https://github.com/azaz-az/holiday-predictor\n")
        sys.exit(1)
