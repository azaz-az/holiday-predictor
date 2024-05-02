"""存储一些程序所需信息的模块。

该模块存储了部分程序运行时所需要的信息。
"""

from enum import Enum
from typing import ClassVar, Dict, Optional, Tuple

class Data:
    """存储一些程序所需信息的类。

    该类存储了部分程序运行时需要的信息。
    """

    # 以下这四行存储的是所有3天假期的放假安排，这些数据代表与节日当天差的天数
    HLD_3DAYS_DAYS: ClassVar[Tuple[int, int, int, int, int, int, int]] = \
    (3, 3, 1, 3, 3, 3, 3)
    HLD_3DAYS_START_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (-2, -2,  0,  0,  0,  0, -1)
    HLD_3DAYS_END_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (0, 0, 0, 2, 2, 2, 1)
    HLD_3DAYS_LIEU1_DELTA_DAY: ClassVar[Tuple[
        Optional[int], Optional[int], Optional[int], Optional[int],
        Optional[int], Optional[int], Optional[int]
    ]] = (None, -3, None, 3, None, None, None)

    # 以下这五行存储的是五一假期的放假安排，这些数据代表与节日当天差的天数
    INTERNATIONAL_LABOURS_DAY_DAYS: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (5, 5, 5, 5, 5, 5, 5)
    INTERNATIONAL_LABOURS_DAY_START_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (-2, -3, 0, 0, 0, 0, -1)
    INTERNATIONAL_LABOURS_DAY_END_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (2, 1, 4, 4, 4, 4, 3)
    INTERNATIONAL_LABOURS_DAY_LIEU1_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (-8, -9, -3, -4, -5, -6, -7)
    INTERNATIONAL_LABOURS_DAY_LIEU2_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (5, 4, 10, 9, 8, 7, 6)

    # 以下这五行存储的是春节假期的放假安排，这些数据代表与节日当天差的天数
    SPRING_FESTIVAL_DAYS: ClassVar[Tuple[int, int, int, int, int, int, int]] =\
    (8, 8, 8, 8, 8, 8, 8)
    SPRING_FESTIVAL_START_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (-2, 0, 0, 0, 0, 0, -1)
    SPRING_FESTIVAL_END_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (5, 7, 7, 7, 7, 7, 6)
    SPRING_FESTIVAL_LIEU1_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (-8, -2, -3, -4, 8, -6, -7)
    SPRING_FESTIVAL_LIEU2_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (6, 11, 10, 9, 9, 8, 7)

    help: ClassVar[str] = (
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
        "    --spring-festival 或 -sf ------------- 预测春节假期。\n"
        "    --qing-ming 或 -qm ------------------- 预测清明假期。\n"
        "    --international-labours-day 或 -ild -- 预测五一假期。\n"
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
        "    fc 2047 -ild --do-not-output-notes - 预测 2061 年的五一假期，且不输出 Note 信息。\n"
        "\n"
        "注意：\n"
        "    由于部分兼容性问题，forecastlist 或 fclist 指令已从 Holiday Predictor / 假期预测器 中移除。\n"
    )

    help_i18n: ClassVar[Dict[str, str]] = {"zh_hans": help}

    international_labours_day_note: ClassVar[str] = """NOTE: 五一的放假方式经历过两次修改。
      最早，五一放假七天；后来，五一放假三天；时至今日，五一放假五天。
      在本程序中，统一以放假五天为准。
      因此，在预测以前的五一假期时，本程序给出的结果并不准确。\n"""

    spring_festival_note: ClassVar[str] = """NOTE: 春节的放假方式经历过两次修改。
      最早，除夕不放假，且假期共7天；后来，除夕放假，且假期共7天；时至今日，除夕不放假，但放假8天。
      在本程序中，统一以除夕不放假，但放假8天为准。
      因此，在预测以前的春节假期时，本程序给出的结果并不准确。
      并且，由于在本项目制作春节部分时是第一个除夕不放假，连放8天的春节，没有过往的历史可以参考，
      在预测未来的春节假期时，也不一定准确。"""

    international_labours_day_note_i18n: ClassVar[Dict[str, str]] = {
        "zh_hans": international_labours_day_note
    }

    spring_festival_note_i18n: ClassVar[Dict[str, str]] = {
        "zh_hans": spring_festival_note
    }

class HolidayType(Enum):
    NATIONAL_DAY = "-nd"
    ND = "-nd"
    NEW_YEAR = "-ny"
    NY = "-ny"
    SPRING_FESTIVAL = "-sf"
    SF = "-sf"
    QING_MING = "-qm"
    QM = "-qm"
    DUAN_WU = "-dw"
    DW = "-dw"
    INTERNATIONAL_LABOURS_DAY = "-ild"
    ILD = "-ild"
    MID_AUTUMN = "-ma"
    MA = "-ma"
