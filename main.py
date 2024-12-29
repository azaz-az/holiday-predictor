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

__all__ = ["calculation", "calculation_forecast_list", "calculation_forecast_nearly"]

import datetime

from typing import Optional, Tuple, List

from zhdate import ZhDate  # type: ignore

from holiday_predictor import CalculationUtil
from text_info import TextInfo


class ForecastList:
    """处理 ForecastList 请求的类.

    Args:
        ForecastList.假期名(起始年份: int, 结束年份: int)

    Returns:
        范围内的所有指定假期的放假、调休日期: List

        列表每一项的详细格式见下:

        <假期开始日期>: datetime, <假期结束日期>: datetime, [调休日期1(若有)]: datetime, [调休日期2(若有)]: datetime
    """

    @staticmethod
    def new_year(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-ny"]))
        return results

    @staticmethod
    def spring_festival(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-sf"]))
        return results

    @staticmethod
    def qing_ming(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-qm"]))
        return results

    @staticmethod
    def international_labours_day(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-ild"]))
        return results

    @staticmethod
    def duan_wu(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-dw"]))
        return results

    @staticmethod
    def mid_autumn(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-ma"]))
        return results

    @staticmethod
    def national_day(start_year: int, end_year: int):
        results: list = []
        for i in range(end_year - start_year + 1):
            results.append(calculation(["fc", start_year + i, "-nd"]))
        return results


def calculation_forecast_list(given_list: List[str]) -> str:
    """该函数用于计算 forecast list 形式的多个假期日期和调休日期。

    该函数计算指定的年份范围 中，用户输入的假期的年份范围和这些假期的调休情况。

    Args:
        given_list (list[str]): 传入用户的输入，这是以用空格拆分后的列表形式输入的。

    Returns:
        str: 返回需要打印的输出字符串。
    """

    start_year: int = int(given_list[1])
    end_year: int = int(given_list[2])
    holiday_name: str = str(given_list[3])

    if holiday_name in ("--national-day", "-nd"):
        return '\n'.join(ForecastList.national_day(start_year, end_year))
    if holiday_name in ("--new-year", "-ny"):
        return '\n'.join(ForecastList.new_year(start_year, end_year))
    if holiday_name in ("--spring-festival", "-sf"):
        return '\n'.join(ForecastList.spring_festival(start_year, end_year))
    if holiday_name in ("--qing-ming", "-qm"):
        return '\n'.join(ForecastList.new_year(start_year, end_year))
    if holiday_name in ("--international-labours-day", "-ild"):
        return '\n'.join(ForecastList.international_labours_day(start_year, end_year))
    if holiday_name in ("--duan-wu", "-dw"):
        return '\n'.join(ForecastList.duan_wu(start_year, end_year))
    if holiday_name in ("--mid-autumn", "-ma"):
        return '\n'.join(ForecastList.mid_autumn(start_year, end_year))


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
            print(TextInfo.spring_festival_note)
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
            print(TextInfo.international_labours_day_note)
        international_labours_day_result: Optional[Tuple[
            datetime.datetime, datetime.datetime, datetime.datetime
        ]] = CalculationUtil.international_labours_day(forecast_year)
        if international_labours_day_result is None:
            return ("错误的输入。给定年份 {year} "
                    "不存在五一假期。".format(year=forecast_year))
        hld_startdate, hld_enddate, lieu_1 = \
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
            start_dateofweek=TextInfo.INT_TO_WEEKDAY[hld_startdate.weekday()],
            end=hld_enddate,
            end_dateofweek=TextInfo.INT_TO_WEEKDAY[hld_enddate.weekday()],
            lieu1=lieu_1.date(),
            lieu1_dateofweek=TextInfo.INT_TO_WEEKDAY[lieu_1.weekday()],
            lieu2=lieu_2.date(),
            lieu2_dateofweek=TextInfo.INT_TO_WEEKDAY[lieu_2.weekday()],
            day=hld_days
        ))
    if lieu_1 is not None:
        return ("假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。"
                "调休时间为 {lieu}（星期{lieu_dateofweek}）。".format(
            start=hld_startdate,
            start_dateofweek=TextInfo.INT_TO_WEEKDAY[hld_startdate.weekday()],
            end=hld_enddate,
            end_dateofweek=TextInfo.INT_TO_WEEKDAY[hld_enddate.weekday()],
            lieu=lieu_1.date(),
            lieu_dateofweek=TextInfo.INT_TO_WEEKDAY[lieu_1.weekday()],
            day=hld_days
        ))
    return "假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。".format(
        start=hld_startdate,
        start_dateofweek=TextInfo.INT_TO_WEEKDAY[hld_startdate.weekday()],
        end=hld_enddate,
        end_dateofweek=TextInfo.INT_TO_WEEKDAY[hld_enddate.weekday()],
        day=hld_days
    )


def calculation_forecast_nearly() -> str:
    if CalculationUtil.NearlyNext.today() is None:
        return calculation(['forecast', datetime.datetime.today().year + 1, '--new-year'])
    else:
        return (calculation(['forecast',
                             datetime.datetime.today().year,
                             '--' + str(CalculationUtil.NearlyNext.today()[1].replace('_', '-'))]))


if __name__ == "__main__":
    print(calculation_forecast_nearly())
