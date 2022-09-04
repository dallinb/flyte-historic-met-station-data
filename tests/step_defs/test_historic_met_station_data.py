"""Met Office Historical Station Data feature tests."""
import logging
import historical.utils

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from historical.avsc import OBSERVATION_AVRO_SCHEMA
from historical.observation import Observation
from historical.station import Station


def float_or_none(value: str):
    """
    Parse a string.

    Parameters
    ----------
    value : str
        The expected value.

    Returns
    -------
    object
        A float if the value is not a blank string or None otherwise.
    """
    value = value.strip()

    if value == '' or value == '---':
        return None
    else:
        return float(value)


@scenario('../features/historic-met-station-data.feature', 'Observation Parsing')
def test_observation_parsing():
    """Observation Parsing."""


@given(parsers.parse('input line is {line}'), target_fixture='observation')
def input_line_is_line(line):
    """input line is <line>."""
    return Observation(line)


@when('line is parsed')
def line_is_parsed(observation):
    """line is parsed."""
    station = Station('Fulchester', 'http://foo')
    assert station.name == 'Fulchester'
    logger = historical.utils.get_logger('foo')
    assert logger.level == logging.WARN
    args = historical.utils.command_line_interface([])
    observation.station_name('Fulchester')
    assert not args.__dict__['verbose']
    assert str(observation)
    assert observation.to_dict()


@then(parsers.parse('af is {af}'))
def af_is_af(af, observation):
    """af is <af>."""
    af = float_or_none(af)
    assert af == observation.af
    assert OBSERVATION_AVRO_SCHEMA


@then(parsers.parse('af_is_estimated is {af_is_estimated}'))
def af_is_estimated_is_af_is_estimated(af_is_estimated, observation):
    """af is estimated is <af_is_estimated>."""
    af_is_estimated = (af_is_estimated == 'True')
    assert af_is_estimated == observation.af_is_estimated


@then(parsers.parse('is_provisional is {is_provisional}'))
def is_provisional_is_is_provisional(is_provisional, observation):
    """is provisional is <is_provisional>."""
    is_provisional = (is_provisional == 'True')
    assert is_provisional == observation.is_provisional


@then(parsers.parse('month is {month:d}'))
def month_is_month(month, observation):
    """month is <month>."""
    assert month == observation.month


@then(parsers.parse('rain is {rain}'))
def rain_is_rain(rain, observation):
    """rain is <rain>."""
    rain = float_or_none(rain)
    assert rain == observation.rain


@then(parsers.parse('rain_is_estimated is {rain_is_estimated}'))
def rain_is_estimated_is_rain_is_estimated(rain_is_estimated, observation):
    """rain is estimated is <rain_is_estimated>."""
    rain_is_estimated = (rain_is_estimated == 'True')
    assert rain_is_estimated == observation.rain_is_estimated


@then(parsers.parse('sun is {sun}'))
def sun_is_sun(sun, observation):
    """sun is <sun>."""
    sun = float_or_none(sun)
    assert sun == observation.sun


@then(parsers.parse('sun_instrument is {sun_instrument}'))
def sun_instrument_is_sun_instrument(sun_instrument, observation):
    """sun_instrument is <sun_instrument>."""
    if sun_instrument == '---':
        sun_instrument = None
    assert sun_instrument == observation.sun_instrument


@then(parsers.parse('sun_is_estimated {sun_is_estimated}'))
def sun_is_estimated_is_sun_is_estimated(sun_is_estimated, observation):
    """sun is estimated is <sun_is_estimated>."""
    sun_is_estimated = (sun_is_estimated == 'True')
    assert sun_is_estimated == observation.sun_is_estimated


@then(parsers.parse('tmax is {tmax}'))
def tmax_is_tmax(tmax, observation):
    """tmax is <tmax>."""
    tmax = float_or_none(tmax)
    assert tmax == observation.tmax


@then(parsers.parse('tmax_is_estimated is {tmax_is_estimated}'))
def tmax_is_estimated_is_tmax_is_estimated(tmax_is_estimated, observation):
    """tmax is estimated is <tmax_is_estimated>."""
    tmax_is_estimated = (tmax_is_estimated == 'True')
    assert tmax_is_estimated == observation.tmax_is_estimated


@then(parsers.parse('tmin is {tmin}'))
def tmin_is_tmin(tmin, observation):
    """tmin is <tmin>."""
    tmin = float_or_none(tmin)
    assert tmin == observation.tmin


@then(parsers.parse('tmin_is_estimated is {tmin_is_estimated}'))
def tmin_is_estimated_is_tmin_is_estimated(tmin_is_estimated, observation):
    """tmin is estimated is <tmin_is_estimated>."""
    tmin_is_estimated = (tmin_is_estimated == 'True')
    assert tmin_is_estimated == observation.tmin_is_estimated


@then(parsers.parse('year is {year:d}'))
def year_is_year(year, observation):
    """year is <year>."""
    assert year == observation.year
