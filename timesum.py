"""Combines minutes and seconds into a single fractional number of minutes."""
from typing import NewType, Tuple
from fractions import Fraction
from math import floor

MinutesAndSeconds = NewType('MinutesAndSeconds', Fraction)
HoursMinutesSeconds = NewType('HoursMinutesSeconds', Tuple[int, int, int])


def calculate_earthly_time(entered_ms: MinutesAndSeconds) -> HoursMinutesSeconds:
    """Transforms a fractional representation of minutes into hours, minutes and seconds.
    Returns a tuple (hours, minutes, seconds) with the type HoursMinutesSeconds."""
    minutes_and_hours = floor(entered_ms)
    seconds = floor((entered_ms - minutes_and_hours) * 60)
    hours = floor(minutes_and_hours / 60)
    minutes = minutes_and_hours - 60 * hours
    return HoursMinutesSeconds((hours, minutes, seconds))


def earthly_time_to_time_frac(hms: HoursMinutesSeconds) -> MinutesAndSeconds:
    return hms[0] * 60 + hms[1] + Fraction(hms[2], 60)


def time_frac(minutes: int, seconds: int) -> MinutesAndSeconds:
    calculated_duration = MinutesAndSeconds(Fraction(minutes * 60 + seconds, 60))
    return calculated_duration


if __name__ == '__main__':
    _done = False
    _end_sum = time_frac(0, 0)
    while not _done:
        _minutes = int(input("Enter the number of minutes: "))
        _seconds = int(input("Enter the number of seconds: "))
        _turn_time = time_frac(_minutes, _seconds)
        _end_sum += _turn_time
        #test_input = input("Any more periods of time [Y|N]? ")
        #print("You entered\n", test_input, sep='')
        _done = (input("Any more periods of time [Y|N]? ").upper() != 'Y')
    _result = calculate_earthly_time(_end_sum)
    assert earthly_time_to_time_frac(_result) == _end_sum
    print("That's", _result[0], "hours,", _result[1], "minutes, and", _result[2], "seconds.")
