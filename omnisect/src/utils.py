import datetime

import dateutil.parser


class DatetimeUtils:
    @staticmethod
    def now() -> datetime.datetime:
        return datetime.datetime.now(datetime.UTC)

    @staticmethod
    def now_iso_str() -> str:
        return DatetimeUtils.now().isoformat(timespec="milliseconds")

    @staticmethod
    def parse_iso_str(iso_date: str) -> datetime.datetime:
        return dateutil.parser.parse(iso_date)
