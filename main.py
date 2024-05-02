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

__all__ = ["calculation"]

from typing import List, Optional

import datetime

from zhdate import ZhDate # type: ignore

from data import Data
#尝试启用GUI显示模式
method_UI=True
try:
    import easygui
except:
    method_UI=False#进入兼容模式(调试模式)




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
    hld_startdate: Optional[datetime.datetime] = None # type: ignore
    hld_enddate: Optional[datetime.datetime] = None
    hld_days: int = 0

    # 这两个变量定义调休的日期。在随后会被修改，用 "None" 来判定是否有调休出现。
    lieu_1: Optional[datetime.datetime] = None
    lieu_2: Optional[datetime.datetime] = None

    if holiday_name in ("--national-day", "-nd"):  # 该部分用于处理国庆假期的调休预测。
        if forecast_year < 1949:
            return ("错误的输入。给定年份 {year} "
                    "不存在国庆假期。".format(year=forecast_year))
        # 下述代码对中秋节、国庆节的日期进行运算。
        mid_date: datetime.datetime = ZhDate(
            forecast_year, 8, 15
        ).to_datetime()  # 该变量是中秋节的日期。
        nati_date = datetime.datetime(
            forecast_year, 10, 1
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
                days=hld_start_dateofweek+1
            )
            lieu_2 = hld_enddate + datetime.timedelta(days=5-hld_end_dateofweek)

    elif holiday_name in ("--new-year", "-ny"):  # 该部分用于处理元旦假期的调休预测。
        new_year_date: datetime.datetime = datetime.datetime(
            year=forecast_year, month=1, day=1
        )
        new_year_dateofweek: int = new_year_date.weekday()
        hld_days = Data.hld_3days_days[new_year_dateofweek]
        hld_startdate = \
            new_year_date + datetime.timedelta(
                Data.hld_3days_start_delta_day[new_year_dateofweek])
        
        hld_enddate = \
            new_year_date + datetime.timedelta(Data.hld_3days_end_delta_day[new_year_dateofweek])
        
        if Data.hld_3days_lieu1_delta_day[new_year_dateofweek] is not None:
            lieu_1 = \
                new_year_date + datetime.timedelta(
                    Data.hld_3days_lieu1_delta_day[new_year_dateofweek]) # type: ignore

    elif holiday_name in ("--qing-ming", "-qm"):  # 该部分用于处理清明假期的调休预测。
        qing_ming_date: datetime.datetime
        if forecast_year % 4 == 0:
            if forecast_year % 400 == 0:
                qing_ming_date = datetime.datetime(year=forecast_year, month=4, day=4)
            elif forecast_year % 100 == 0:
                qing_ming_date = datetime.datetime(year=forecast_year, month=4, day=5)
            else:
                qing_ming_date = datetime.datetime(year=forecast_year, month=4, day=4)
        else:
            qing_ming_date = datetime.datetime(year=forecast_year, month=4, day=5)
        qing_ming_dateofweek = qing_ming_date.weekday()
        # 下述代码对清明假期的调休进行运算。
        hld_days = Data.hld_3days_days[qing_ming_dateofweek]
        hld_startdate = \
            qing_ming_date + datetime.timedelta(
                Data.hld_3days_start_delta_day[qing_ming_dateofweek])
        
        hld_enddate = \
            qing_ming_date + datetime.timedelta(Data.hld_3days_end_delta_day[qing_ming_dateofweek])
        
        if Data.hld_3days_lieu1_delta_day[qing_ming_dateofweek] is not None:
            lieu_1 = \
                qing_ming_date + datetime.timedelta(
                    Data.hld_3days_lieu1_delta_day[qing_ming_dateofweek]) # type: ignore

    elif holiday_name in ("--duan-wu", "-dw"):  # 该部分用于处理端午假期的调休预测。
        duan_wu_date: datetime.datetime = ZhDate(forecast_year, 5, 5).to_datetime()
        duan_wu_dateofweek: int = duan_wu_date.weekday()
        # 下述代码对端午假期的调休进行运算。
        hld_days = Data.hld_3days_days[duan_wu_dateofweek]
        hld_startdate = \
            duan_wu_date + datetime.timedelta(
                Data.hld_3days_start_delta_day[duan_wu_dateofweek])
        
        hld_enddate = \
            duan_wu_date + datetime.timedelta(Data.hld_3days_end_delta_day[duan_wu_dateofweek])
        
        if Data.hld_3days_lieu1_delta_day[duan_wu_dateofweek] is not None:
            lieu_1 = \
                duan_wu_date + datetime.timedelta(
                    Data.hld_3days_lieu1_delta_day[duan_wu_dateofweek]) # type: ignore

    elif holiday_name in ("--international-labours-day", "-ilb"):  # 该部分用于处理五一假期的调休预测。
        if not '--do-not-output-notes' in given_list:
            print(Data.international_labours_day_note)
        international_labours_day_date: datetime.datetime = datetime.datetime(year=forecast_year, month=5, day=1)
        international_labours_day_dateofweek: int = international_labours_day_date.weekday()
        # 下述代码对五一假期的调休进行运算。
        hld_days = Data.international_labours_day_days[international_labours_day_dateofweek]
        hld_startdate = \
            international_labours_day_date + datetime.timedelta(
                Data.international_labours_day_start_delta_day[international_labours_day_dateofweek])  
        hld_enddate = \
            international_labours_day_date + datetime.timedelta(Data.international_labours_day_end_delta_day[international_labours_day_dateofweek])
        lieu_1 = \
            international_labours_day_date + datetime.timedelta(
                Data.international_labours_day_lieu1_delta_day[international_labours_day_dateofweek])
        lieu_2 = \
            international_labours_day_date + datetime.timedelta(
                Data.international_labours_day_lieu2_delta_day[international_labours_day_dateofweek])

    elif holiday_name in ("--mid-autumn", "-ma"):  # 该部分用于处理中秋假期的调休预测。
        mid_autumn_date: datetime.datetime = ZhDate(forecast_year, 8, 15).to_datetime()
        mid_autumn_dateofweek: int = mid_autumn_date.weekday()
        # 下述代码对中秋假期的调休进行运算。
        if calculation(['fc', str(forecast_year), '-nd', '--only-return-days']) == str(8):
            if '--only-return-days' in given_list:
                return calculation(['fc', str(forecast_year), '-nd', '--only-return-days'])
            else:
                return calculation(['fc', str(forecast_year), '-nd'])
        hld_days = Data.hld_3days_days[mid_autumn_dateofweek]
        hld_startdate = \
            mid_autumn_date + datetime.timedelta(
                Data.hld_3days_start_delta_day[mid_autumn_dateofweek])
        
        hld_enddate = \
            mid_autumn_date + datetime.timedelta(Data.hld_3days_end_delta_day[mid_autumn_dateofweek])
        
        if Data.hld_3days_lieu1_delta_day[mid_autumn_dateofweek] is not None:
            lieu_1 = \
                mid_autumn_date + datetime.timedelta(
                    Data.hld_3days_lieu1_delta_day[mid_autumn_dateofweek]) # type: ignore
        
    else:
        return "不存在的参数 {name}。".format(name=holiday_name)

    if '--only-return-days' in given_list:
        return (str(hld_days))
    elif lieu_1 is not None and lieu_2 is not None:
        return ("假期由 {start} 起，直到 {end}，共{day}天。\n调休时间为 "
                "{lieu1} 和 {lieu2}。".format(
                   start=hld_startdate,
                   end=hld_enddate,
                   lieu1=lieu_1.date(),
                   lieu2=lieu_2.date(),
                   day=hld_days
               ))
    elif lieu_1 is not None:
        return ("假期由 {start} 起，直到 {end}，共{day}天。\n调休时间为 "
                "{lieu}。".format(
                   start=hld_startdate,
                   end=hld_enddate,
                   lieu=lieu_1.date(),
                   day=hld_days
               ))
    else:
        return "假期由 {start} 起，直到 {end}，共{day}天。".format(
        start=hld_startdate, end=hld_enddate, day=hld_days
        )
def Debug_method():
    global input_list,Data,LIEU_DATE_1,LIEU_DATE_2
    execution_flag: bool = \
    False  # 该变量用于报告用户输入是否命中某个指令。在下面的代码中，用户输入触发对任意指令的处理后，该变量即被设置为 True。
    try:  # 这段代码判定是否让程序进入调试模式。调试模式默认处于关闭状态。
        input_list = input("> ").lower().split(" ")
    except (KeyboardInterrupt, EOFError):
        print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。\n")
        return 0
    if input_list[0] in ("forecast", "fc"):  # 处理用户发起的 forecast 指令请求。
        try:
            print(calculation(input_list))
        except (KeyboardInterrupt, EOFError):
            print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。")
            return 0
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
            return 1
    if input_list[0] == "help":
        print(Data.help)
        execution_flag = True # pylint: disable = C0103
        return 1

    if input_list[0] in ("exit", "quit"):
        return 0
    if not execution_flag:
        print('未知的指令 {unknown}。'
                  '键入 "help" 以查看帮助。'.format(unknown=input_list[0]))
        print('\n如果你不会使用该程序，键入 "help" 以查看帮助。')
        print("如果无法定位程序未按预期运行的原因，请向我们报告错误。"
                  "https://github.com/azaz-az/holiday-predictor\n")
        execution_flag = True  # pylint: disable = C0103
        return 1

'''此处将定义原二级变量在GUI中的赋值'''
note_on=True
notonly_days=True
'''二级变量已迁移至设置中开关'''

def GUIs_method():
    global input_list,Data,LIEU_DATE_1,LIEU_DATE_2,method_UI,note_on,notonly_days
    execution_flag:bool= \
    False  # 该变量用于报告用户输入是否命中某个指令。在下面的代码中，用户输入触发对任意指令的处理后，该变量即被设置为 True。

    Maincc=easygui.buttonbox("欢迎使用假期预测器",Data.title_text,Data.main_cs)
    if Maincc==Data.main_cs[0]:
        Year=easygui.enterbox("请输入查询的年份",Data.title_text)
        HoliDay=easygui.choicebox("查询哪个节日",Data.title_text,Data.hd_cn_cs)
        if (HoliDay in Data.hd_cn_cs)==False:
            return 1
        HoliDay=Data.hd_dos_cs[Data.hd_cn_cs.index(HoliDay)]
        final_list=[]
        if notonly_days==False:
            final_list.append("--only-return-days")
        if note_on:
            final_list.append("--do-not-output-notes")
        input_list=["fc",Year,HoliDay,final_list]
        easygui.msgbox(calculation(input_list))
    elif Maincc==Data.main_cs[1]:
        method_UI=False
        return 1
    elif Maincc==Data.main_cs[2]:
        settingcc=easygui.buttonbox("欢迎来到假期预测器的设置界面",Data.title_text,Data.setting_cs)
        if settingcc==Data.setting_cs[0]:
            easygui.msgbox(Data.thk_list,Data.title_text)
        elif settingcc==Data.setting_cs[1]:
            if notonly_days:
                nd="全写(包括调休和假期时间段)"
            else:
                nd="仅显示天数"
            mlc=easygui.buttonbox('''要启用哪些选择(如无必要请务必全部启用) \n
                                  结果输出模式:{dys}\n 
                                  显示笔记:{note} \n
                                  点击下列选项进行更改
                                  '''.format(note=Data.transfer(note_on),dys=nd)
                                  ,Data.title_text,Data.sec_agr_cs)
            if mlc==Data.sec_agr_cs[0]:
                notonly_days=easygui.ynbox("选择输出模式",Data.title_text,("全写(包括调休和假期时间段)","仅显示天数"))
            if mlc==Data.sec_agr_cs[1]:
                note_on=easygui.ynbox("选择笔记显示方式",Data.title_text,("开启","关闭"))
                print(note_on)
    elif Maincc==None or Maincc==Data.main_cs[3]:
        return 0







if __name__ == "__main__":
    print("\nHoliday Predictor / 假期预测器 - 基于 Python 的调休预测工具\n键入 help 以查看帮助。")

    LIEU_DATE_1 = LIEU_DATE_2 = 0
    input_list: List[str] = []  # 初始化 input_list
    while True:
        result=1
        if method_UI:
            result = GUIs_method()
        else:
            result = Debug_method()
        if result ==0:
            break