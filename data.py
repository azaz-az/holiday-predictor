"""存储一些程序所需信息的模块。

该模块存储了部分程序运行时所需要的信息。
"""


class Data:
    """存储一些程序所需信息的类。

    该类存储了部分程序运行时需要的信息。
    """

    # 以下这四行存储的是所有3天假期的放假安排，这些数据代表与节日当天差的天数
    hld_3days_days            = [ 3,  3,  1,  3,  3,  3,  3]
    hld_3days_start_delta_day = [-2, -2,  0,  0,  0,  0, -1]
    hld_3days_end_delta_day   = [ 0,  0,  0,  2,  2,  2,  1]
    hld_3days_lieu1_delta_day = [None, -3, None,  3, None, None, None]

    # 以下这五行存储的是五一假期的放假安排，这些数据代表与节日当天差的天数
    international_labours_day_days            = [ 5,  5,  5,  5,  5,  5,  5]
    international_labours_day_start_delta_day = [-2, -3,  0,  0,  0,  0, -1]
    international_labours_day_end_delta_day   = [ 2,  1,  4,  4,  4,  4,  3]
    international_labours_day_lieu1_delta_day = [-8, -9, -3, -4, -5, -6, -7]
    international_labours_day_lieu2_delta_day = [ 5,  4, 10,  9,  8,  7,  6]

    help = (
        "\nHoliday Predictor / 假期预测器 帮助文档\n\n"
        "用法：\n"
        "    [command] [year] [argument] [second_argument]\n"
        "\n"
        "指令 (command)：\n"
        "    forecast 或 fc ---------------- 预测对应年份的假期情况。\n"
        "    quit 或 exit ------------------ 退出程序。\n"
        "\n"
        "参数 (argument)：\n"
        "    --new-year 或 -ny -------------------- 预测元旦假期。\n"
        "    --qing-ming 或 -qm ------------------- 预测清明假期。\n"
        "    --international-labours-day 或 -ilb -- 预测五一假期。\n"
        "    --duan-wu 或 -dw --------------------- 预测端午假期。\n"
        "    --mid-autumn 或 -ma ------------------ 预测中秋假期。\n"
        "    --national-day 或 -nd ---------------- 预测国庆假期。\n"
        "\n"
        "第二参数 (second_argument)：\n"
        "    --only-return-days ------------ 仅输出假期天数。\n"
        "    --do-not-output-notes --------- 不要输出 Note 信息。\n"
        "\n"
        "示例：\n"
        "    forecast 2024 --national-day ------ 预测 2024 年的国庆假期。\n"
        "    （该示例与 fc 2024 -nd 等效。）\n"
        "    forecast 2085 --new-year ---------- 预测 2085 年的元旦假期。\n"
        "    （该示例与 fc 2085 -ny 等效。）\n"
        "    forecast 2048 --qing-ming --------- 预测 2048 年的清明假期。\n"
        "    （该示例与 fc 2048 -qm 等效。）\n"
        "    forecast 2032 --duan-wu ----------- 预测 2032 年的端午假期。\n"
        "    （该示例与 fc 2032 -dw 等效。）\n"
        "    forecast 2061 --mid-autumn -------- 预测 2061 年的中秋假期。\n"
        "    （该示例与 fc 2061 -ma 等效。）\n"
        "    fc 2061 -ma --only-return-days ---- 预测 2061 年的中秋假期，且只输出假期天数。\n"
        "    fc 2047 -ilb --do-not-output-notes - 预测 2061 年的五一假期，且不输出 Note 信息。\n"
        "\n"
        "注意：\n"
        "    由于部分兼容性问题，forecastlist 或 fclist 指令已从 Holiday Predictor / 假期预测器 中移除。\n"
    )

    international_labours_day_note = ("NOTE: 五一的放假方式经历过两次修改。\n"
                    "      最早，五一放假七天；后来，五一放假三天；最后，五一放假五天。\n"
                    "      在本程序中，统一以放假五天为准。\n"
                    "      因此，在预测以前的五一假期时，本程序给出的结果并不准确。\n"
    )
