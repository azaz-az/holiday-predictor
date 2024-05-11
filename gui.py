#!python3

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
from typing import Optional, Tuple
import datetime
import tkinter as tk

from data import Data, HolidayType
from main import CalculationUtil


def calculation(years: str, holiday_type: HolidayType,
                only_return_days: bool = False) -> str:
    try:
        year = int(years)
    except ValueError:
        return "输入的年份有误!"
    if type(holiday_type) is not HolidayType:
        raise AssertionError
    hld_startdate: Optional[datetime.datetime] = None  # type: ignore
    hld_enddate: Optional[datetime.datetime] = None
    # 这两个变量定义调休的日期。在随后会被修改，用 "None" 来判定是否有调休出现。
    lieu_1: Optional[datetime.datetime] = None
    lieu_2: Optional[datetime.datetime] = None
    try:
        if holiday_type == HolidayType.ND:  # 该部分用于处理国庆假期的调休预测。
            national_day_result: Optional[Tuple[
                datetime.datetime, datetime.datetime, Optional[datetime.datetime],
                Optional[datetime.datetime]
            ]] = CalculationUtil.national_day(year)
            if national_day_result is None:
                return ("错误的输入。给定年份 {year} "
                        "不存在国庆假期。".format(year=year))
            hld_startdate, hld_enddate, lieu_1, lieu_2 = national_day_result
        elif holiday_type == HolidayType.NY:  # 该部分用于处理元旦假期的调休预测。
            hld_startdate, hld_enddate, lieu_1 = \
                CalculationUtil.new_year(year)
        elif holiday_type == HolidayType.SF:  # 该部分用于处理春节假期的调休预测。
            hld_startdate, hld_enddate, lieu_1, lieu_2 = \
                CalculationUtil.spring_festival(year)
        elif holiday_type == HolidayType.QM:  # 该部分用于处理清明假期的调休预测。
            hld_startdate, hld_enddate, lieu_1 = \
                CalculationUtil.qing_ming(year)
        elif holiday_type == HolidayType.DW:  # 该部分用于处理端午假期的调休预测。
            hld_startdate, hld_enddate, lieu_1 = \
                CalculationUtil.duan_wu(year)
        elif holiday_type == HolidayType.ILD:  # 该部分用于处理五一假期的调休预测。
            international_labours_day_result: Optional[Tuple[
                datetime.datetime, datetime.datetime, datetime.datetime,
                datetime.datetime
            ]] = CalculationUtil.international_labours_day(year)
            if international_labours_day_result is None:
                return ("错误的输入。给定年份 {year} "
                        "不存在五一假期。".format(year=year))
            hld_startdate, hld_enddate, lieu_1, lieu_2 = \
                international_labours_day_result
        elif holiday_type == HolidayType.MA:  # 该部分用于处理中秋假期的调休预测。
            hld_startdate, hld_enddate, lieu_1, lieu_2 = \
                CalculationUtil.mid_autumn(year)
    except Exception as e:
        return "程序未按预期进行。抛出了异常:\n{error!r}".format(error=e)
    hld_days: int = (hld_enddate - hld_startdate).days + 1  # type: ignore
    if only_return_days:
        return str(hld_days)  # type: ignore
    if lieu_1 is not None and lieu_2 is not None:
        return ("假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。"
                "调休时间为 {lieu1}（星期{lieu1_dateofweek}）和 {lieu2}（星期{lieu2_dateofweek}）。".format(
            start=hld_startdate,
            start_dateofweek=Data.INT_TO_WEEKDAY[hld_startdate.weekday()],  # type: ignore
            end=hld_enddate,
            end_dateofweek=Data.INT_TO_WEEKDAY[hld_enddate.weekday()],  # type: ignore
            lieu1=lieu_1.date(),
            lieu1_dateofweek=Data.INT_TO_WEEKDAY[lieu_1.weekday()],
            lieu2=lieu_2.date(),
            lieu2_dateofweek=Data.INT_TO_WEEKDAY[lieu_2.weekday()],
            day=hld_days  # type: ignore
        ))
    if lieu_1 is not None:
        return ("假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。"
                "调休时间为 {lieu}（星期{lieu_dateofweek}）。".format(
            start=hld_startdate,
            start_dateofweek=Data.INT_TO_WEEKDAY[hld_startdate.weekday()],  # type: ignore
            end=hld_enddate,
            end_dateofweek=Data.INT_TO_WEEKDAY[hld_enddate.weekday()],  # type: ignore
            lieu=lieu_1.date(),
            lieu_dateofweek=Data.INT_TO_WEEKDAY[lieu_1.weekday()],
            day=hld_days  # type: ignore
        ))
    return "假期由 {start}（星期{start_dateofweek}）起，直到 {end}（星期{end_dateofweek}），共 {day} 天。".format(
        start=hld_startdate,
        start_dateofweek=Data.INT_TO_WEEKDAY[hld_startdate.weekday()],  # type: ignore
        end=hld_enddate,
        end_dateofweek=Data.INT_TO_WEEKDAY[hld_enddate.weekday()],  # type: ignore
        day=hld_days  # type: ignore
    )


root: tk.Tk = tk.Tk()
root.title("Holiday Predictor / 假期预测器")

if __name__ == "__main__":
    fc_result_label: tk.Label = tk.Label(root, text="")
    tk.Label(root, text="请输入要预测假期的年份：").grid(row=0, column=0)
    year_entry: tk.Entry = tk.Entry(root)
    year_entry.grid(row=1, column=0)
    only_return_days_var: tk.BooleanVar = tk.BooleanVar()
    tk.Checkbutton(
        root, text="只显示假期天数", variable=only_return_days_var, offvalue=False,
        onvalue=True
    ).grid(row=9, column=0)
    tk.Button(
        root, text="预测元旦假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.NY, only_return_days_var.get()
            )
        )
    ).grid(row=2, column=0)
    tk.Button(
        root, text="预测春节假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.SF, only_return_days_var.get()
            )
        )
    ).grid(row=3, column=0)
    tk.Button(
        root, text="预测清明假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.QM, only_return_days_var.get()
            )
        )
    ).grid(row=4, column=0)
    tk.Button(
        root, text="预测端午假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.DW, only_return_days_var.get()
            )
        )
    ).grid(row=5, column=0)
    tk.Button(
        root, text="预测五一假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.ILD, only_return_days_var.get()
            )
        )
    ).grid(row=6, column=0)
    tk.Button(
        root, text="预测中秋假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.MA, only_return_days_var.get()
            )
        )
    ).grid(row=7, column=0)
    tk.Button(
        root, text="预测国庆假期", command=lambda: fc_result_label.config(
            text=calculation(
                year_entry.get(), HolidayType.ND, only_return_days_var.get()
            )
        )
    ).grid(row=8, column=0)
    fc_result_label.grid(row=10, column=0, columnspan=2)
    tk.Label(root, text=Data.international_labours_day_note).grid(
        row=0, column=1, rowspan=5
    )
    tk.Label(root, text=Data.spring_festival_note).grid(
        row=5, column=1, rowspan=5
    )
    root.mainloop()
