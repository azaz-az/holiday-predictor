"""这是一个本项目的命令行 Demo 程序。
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

from main import *

import sys

from typing import List

from zhdate import ZhDate  # type: ignore

from text_info import TextInfo

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

        if input_list[0] in ("forecast_list", "fcls"):  # 处理用户发起的 forecast_list 指令请求。
            try:
                print(calculation_forecast_list(input_list))
            except (KeyboardInterrupt, EOFError):
                print("\nHoliday Predictor / 假期预测器 已结束运行。感谢你的使用。")
                break
            except Exception as e:
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
            execution_flag = True

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

        if input_list[0] in ("fcnearly", "forecast_nearly"):
            print(calculation_forecast_nearly())
            execution_flag = True

        if input_list[0] == "help":
            print(TextInfo.help)
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

    if input_list[0] in ("forecast_list", "fcls"):  # 处理用户发起的 forecast_list 指令请求。
        try:
            print(calculation_forecast_list(input_list))
            sys.exit(0)
        except Exception as e:
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
        print(TextInfo.help)
        sys.exit(0)

    else:
        print('未知的指令 {unknown}。'
              '键入 "{arg0} help" 以查看帮助。'.format(unknown=input_list[0],
                                                      arg0=sys.argv[0]))
        print('\n如果你不会使用该程序，键入 "{arg0} help" 以查看帮助。'.format(arg0=sys.argv[0]))
        print("如果无法定位程序未按预期运行的原因，请向我们报告错误。"
              "https://github.com/azaz-az/holiday-predictor\n")
        sys.exit(1)
