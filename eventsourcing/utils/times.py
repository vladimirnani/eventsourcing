import datetime
from decimal import Decimal
import time
from uuid import UUID

import six

if hasattr(datetime, 'timezone'):
    utc_timezone = datetime.timezone.utc
else:
    from datetime import tzinfo, timedelta


    class UTC(tzinfo):
        def utcoffset(self, date_time):
            return timedelta(0)

        def dst(self, date_time):
            return timedelta(0)


    utc_timezone = UTC()


def decimaltimestamp_from_uuid(uuid_arg):
    """
    Return a floating point unix timestamp.

    :param uuid_arg:
    :return: Unix timestamp in seconds, with microsecond precision.
    :rtype: float
    """
    return decimaltimestamp(timestamp_long_from_uuid(uuid_arg) / 1e7)


def timestamp_long_from_uuid(uuid_arg):
    """
    Returns an integer value representing a unix timestamp in tenths of microseconds.

    :param uuid_arg:
    :return: Unix timestamp integer in tenths of microseconds.
    :rtype: int
    """
    if isinstance(uuid_arg, six.string_types):
        uuid_arg = UUID(uuid_arg)
    assert isinstance(uuid_arg, UUID), uuid_arg
    uuid_time = uuid_arg.time
    return uuid_time - 0x01B21DD213814000


def decimaltimestamp(t=None):
    """
    A UNIX timestamp as a Decimal object (exact number type).

    Returns current time when called without args, otherwise
    converts given floating point number ``t`` to a Decimal
    with 9 decimal places.

    :param t: Floating point UNIX timestamp ("seconds since epoch").
    :return: A Decimal with 6 decimal places, representing the
            given floating point or the value returned by time.time().
    """
    t = time.time() if t is None else t
    return Decimal('{:.6f}'.format(t))


def datetime_from_timestamp(t):
    """
    Returns naive UTC datetime from decimal UNIX
    timestamps such as time.time().

    :param t: timestamp, either Decimal or float
    :return: datetime.datetime object
    """
    return datetime.datetime.utcfromtimestamp(float(t))
