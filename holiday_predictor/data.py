from typing import Optional, Tuple, ClassVar


class Data:
    """这个类存储的是模块计算假期安排所需信息的信息
    """

    # 以下这四行存储的是所有3天假期的放假安排，这些数据代表与节日当天差的天数
    HLD_3DAYS_DAYS: ClassVar[Tuple[int, int, int, int, int, int, int]] = \
        (3, 3, 1, 3, 3, 3, 3)
    HLD_3DAYS_START_DELTA_DAY: ClassVar[Tuple[
        int, int, int, int, int, int, int
    ]] = (-2, -2, 0, 0, 0, 0, -1)
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
    SPRING_FESTIVAL_DAYS: ClassVar[Tuple[int, int, int, int, int, int, int]] = \
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

    class NearlyNext:
        """这个子类存储的是与 CalculationUtil.NearlyNext 有关的信息。"""

        HOLIDAY_MAPPING_TABLE: ClassVar[Tuple[
            str, str, str, str, str, str, str, str, str, str, str, str, str, str,
        ]] = ('new_year', 'new_year', 'spring_festival', 'spring_festival',
              'qing_ming', 'qing_ming', 'international_labours_day', 'international_labours_day',
              'duan_wu', 'duan_wu', 'mid_autumn', 'mid_autumn',
              'national_day', 'national_day',)

