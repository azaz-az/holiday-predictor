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

__all__ = ['CalculationUtil']

from typing import Optional, Tuple

import datetime

from zhdate import ZhDate  # type: ignore

from .data import Data


class CalculationUtil:
    """计算假期安排所需的类。

    Args：
        CalculationUtil.假期名(年份)

    Returns：
        datetime: <假期开始日期>, datetime: <假期结束日期>, datetime: [调休日期1(若有)], datetime: [调休日期2(若有)]

    Tip:
        本类的子类 "NearlyNext" 可以预测离某天最近的下一个假期
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
        datetime.datetime, datetime.datetime, datetime.datetime
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
        '''lieu_2: datetime.datetime = \
            international_labours_day_date + datetime.timedelta(
                Data.INTERNATIONAL_LABOURS_DAY_LIEU2_DELTA_DAY[
                    international_labours_day_dateofweek
                ]
            )'''
        return hld_startdate, hld_enddate, lieu_1  #lieu_2

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

    class NearlyNext:
        """预测离某天最近的下一个假期的类。"""

        # 以下这个字典存储的是节日的名称与其对应的函数，方便后续添加其他自定义节日。

        @staticmethod
        def today():
            forecast_date = datetime.datetime.today()
            holidays = {
                'new_year': CalculationUtil.new_year,
                'spring_festival': CalculationUtil.spring_festival,
                'qing_ming': CalculationUtil.qing_ming,
                'duan_wu': CalculationUtil.duan_wu,
                'international_labours_day': CalculationUtil.international_labours_day,
                'mid_autumn': CalculationUtil.mid_autumn,
                'national_day': CalculationUtil.national_day,
            }
            nearest_holiday = None

            def process_holiday(item):
                name, func = item
                start_date, end_date, *_ = func(forecast_date.year)
                return [(name, start_date, end_date, date - forecast_date) for date in (start_date, end_date)]

            processed_dates = sum(map(process_holiday, holidays.items()), [])
            nearest_holiday_data = min(
                filter(lambda x: datetime.timedelta(days=0) <= x[3], processed_dates),
                key=lambda x: x[3],
                default=(None, None, None, None)
            )
            if nearest_holiday_data[0]:
                nearest_holiday = nearest_holiday_data[:3]
            if nearest_holiday:
                return nearest_holiday[1:], nearest_holiday[0]
            return None
