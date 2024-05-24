"""存储一些 Demo 程序所需信息的模块。

该模块存储了部分程序运行时所需要的信息。
"""

from enum import Enum
from typing import ClassVar, Dict, Optional, Tuple


class TextInfo:
    """存储一些程序所需文本信息的类。

    该类存储了部分程序运行时需要的信息。
    """

    INT_TO_WEEKDAY: ClassVar[Tuple[
        str, str, str, str, str, str, str
    ]] = ('一', '二', '三', '四', '五', '六', '日')

    help: ClassVar[str] = (
        "\nHoliday Predictor / 假期预测器 帮助文档\n\n"
        "用法：\n"
        "    [command] [year] [argument] [second_argument]\n"
        "\n"
        "指令 (command)：\n"
        "    forecast 或 fc ---------------- 预测对应年份的假期情况。\n"
        "    forecast_list 或 fcls --------- 预测对应年份的假期情况。\n"
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
        "对于 forecast_list 或 fcls 命令，用法如下：\n"
        "   [command] [start-year] [end-year] [argument]\n"
        "   argument 部分，与 forecast 命令的 argument 相同。\n"
        "\n"
        "示例：\n"
        "   forecast_list 2024 2029 -national-day\n"
        "   （该示例与 fcls 2024 2029 -nd 等效。）\n"
        "注意：\n"
        "   forecast_list 功能在 v0.4.0 中被移除，并在 v0.12.0 中重新加入。\n"
        "   如果你正在使用 v0.4.0 ~ v0.11.x 的版本，则无法使用 forecast_list 功能\n"
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

    international_labours_day_note_en_us: ClassVar[str] = """Note: The International Labour's Day holiday in China 
    has gone through two modifications. At the earliest, International Labour's Day was a seven-day holiday; later, 
    International Labour's Day was a three-day holiday; and now, International Labour's Day is a five-day holiday. In 
    this procedure, the five-day holiday is applied in each case. Therefore, when predicting past International Labor 
    Day holidays, the program gives inaccurate results. \n"""

    spring_festival_note_en_us: ClassVar[str] = """Note: China's Spring Festival holiday has undergone two revisions. 
    At the earliest, there was no holiday on New Year's Eve and the holiday lasted a total of seven days; later, 
    there was a holiday on New Year's Eve and the holiday lasted a total of seven days; to this day, there is no 
    holiday on New Year's Eve and the holiday lasts a total of eight days. In this process, the expression no holiday 
    on New Year's Eve and eight days of holiday was uniformly used. Therefore, when predicting past Chinese New Year 
    holidays, the program gave inaccurate results. In addition, the program did not have past history to refer to 
    when producing the Chinese New Year segment, as it was the first Chinese New Year in which there was no holiday 
    on New Year's Eve and eight consecutive days of holiday. Predicting future Chinese New Year holidays may not be 
    accurate."""

    international_labours_day_note_i18n: ClassVar[Dict[str, str]] = {
        "zh_hans": international_labours_day_note,
        "en_us": international_labours_day_note_en_us
    }

    spring_festival_note_i18n: ClassVar[Dict[str, str]] = {
        "zh_hans": spring_festival_note,
        "en_us": spring_festival_note_en_us
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
