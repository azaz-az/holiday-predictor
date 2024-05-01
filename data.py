"""存储一些程序所需信息的模块。

该模块存储了部分程序运行时所需要的信息。
"""


class Data:
    """存储一些程序所需信息的类。

    该类存储了部分程序运行时需要的信息。
    """

    help = (
        "\nHoliday Predictor / 假期预测器 帮助文档\n\n"
        "用法：\n"
        "    [command] [year] [argument]\n"
        "\n"
        "指令 (command)：\n"
        "    forecast 或 fc ---------------- 预测对应年份的假期情况。\n"
        "    quit 或 exit ------------------ 退出程序。\n"
        "\n"
        "参数 (argument)：\n"
        "    --national-day 或 -nd --------- 预测国庆假期。\n"
        "    --new-year 或 -ny ------------- 预测元旦假期。\n"
        "    --qing-ming 或 -qm ------------ 预测清明假期。\n"
        "    --duan-wu 或 -dw -------------- 预测端午假期。\n"
        "\n"
        "示例：\n"
        "    forecast 2024 --national-day -- 预测 2024 年的国庆假期。\n"
        "    （该示例与 fc 2024 -nd 等效。）\n"
        "    forecast 2085 --new-year ------ 预测 2085 年的元旦假期。\n"
        "    （该示例与 fc 2085 -ny 等效。）\n"
        "    forecast 2048 --qing-ming ----- 预测 2085 年的清明假期。\n"
        "    （该示例与 fc 2048 -qm 等效。）\n"
        "    forecast 2032 --duan-wu ------- 预测 2085 年的端午假期。\n"
        "    （该示例与 fc 2032 -dw 等效。）\n"
        "\n"
        "注意：\n"
        "    由于部分兼容性问题，forecastlist 或 fclist 指令已从 Holiday Predictor / 假期预测器 中移除。\n"
    )

    may_day_note = ("NOTE: 五一的放假方式经历过两次修改。\n"
                    "      最早，五一放假七天；后来，五一放假三天；最后，五一放假五天。\n"
                    "      在本程序中，统一以放假五天为准。\n"
                    "      因此，在预测以前的五一假期时，本程序给出的结果并不准确。\n"
    )
