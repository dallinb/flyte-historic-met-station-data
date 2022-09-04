"""observation.py."""
import json
import re


class Observation:
    """The Observation class."""

    def __init__(self, line: str) -> None:
        """
        Construct an Observation class.

        Parameters
        ----------
        line : str
            A line of data from the Met Office.
        """
        self.line = self.remove_illegal_patterns(line)
        self._station_name = None
        prog = re.compile('[ \t\n\r]+')
        data = prog.split(self.line)
        self.year = int(data[0])
        self.month = int(data[1])
        self.tmax, self.tmax_is_estimated = self.get_possibly_estimated_amount(data[2])
        self.tmin, self.tmin_is_estimated = self.get_possibly_estimated_amount(data[3])
        self.af, self.af_is_estimated = self.get_possibly_estimated_amount(data[4])

        if self.af is not None:
            self.af = int(self.af)

        self.rain, self.rain_is_estimated = self.get_possibly_estimated_amount(data[5])

        self.sun_instrument = None

        if len(data) <= 6:
            self.sun = None
            self.sun_is_estimated = False
        else:
            self.sun, self.sun_is_estimated = self.get_possibly_estimated_amount(data[6])
            self.sun_instrument = self.get_sun_instrument(data[6])

        self.is_provisional = data[-1] == 'Provisional'

    def __str__(self) -> str:
        """
        Convert the object to a printable string.

        Returns
        -------
        str
            A printable representation of the object.
        """
        return self.to_json()

    def get_possibly_estimated_amount(self, field: str):
        """
        Parse a field into a float.  If the field has '*' appended then the value is estimated.

        Parameters
        ----------
        field : str
            The field to be parsed.  If the value is '---' then not enough data was available for that month.
        """
        is_estimated = False

        if field == '---':
            value = None
            return (value, is_estimated)

        if field[-1] == '*':
            is_estimated = True
            value = field[0:-1]
        elif field[-1] == '#':
            value = field[0:-1]
        else:
            value = field

        value = float(value)
        return (value, is_estimated)

    def get_sun_instrument(self, field: str) -> str:
        """
        Return the sun recording instrument.

        If the field ends in a '*' then the

        Parameters
        ----------
        field : str
            The field provided by the Met Office for the hours of the sun recorded.

        Returns
        -------
        str
            One of either None, 'Kipp & Zonen' or 'Campbell Stokes'.
        """
        map = {
            '*': None,
            '-': None,
            '#': 'Kipp & Zonen'
        }

        last_character = field[-1]

        if last_character not in map:
            return 'Campbell Stokes'

        return map[last_character]

    def remove_illegal_patterns(self, line: str) -> str:
        """
        Remove illegal string patterns from the input line of data.

        Some strange patterns have been inserted into the data for some
        observations for some stations.  Examples are:

          Lowestoft 2007-09

        This function ensures all lines are uniform before parsing.

        Parameters
        ----------
        line : str
            The raw input line that may potentially have none specification patterns.

        Returns
        -------
        str
            A clean line.
        """
        invalid_patters = [
            # Patterns that are non-standard, but have made it into the data.
            '$',
            'all data from Whitby',
            'Change to Monckton Ave'
        ]

        for invalid_pattern in invalid_patters:
            line = line.replace(invalid_pattern, '')

        return line

    def station_name(self, station_name: str = None) -> str:
        """
        Get or set the station name.

        Parameters
        ----------
        station_name : str, optional
            The name of the station., by default None

        Returns
        -------
        str
            The name of the station.
        """
        if station_name is not None:
            self._station_name = station_name

        return self._station_name

    def to_dict(self) -> dict:
        """
        Convert the contents of the objecct to a dictionary.

        Returns
        -------
        dict
            A dictionary generated from the to_json method.
        """
        return json.loads(self.to_json())

    def to_json(self) -> str:
        """
        Convert the contents of the object to a JSON string.

        Returns
        -------
        str
            A JSON string.
        """
        data = {
            'year': self.year,
            'month': self.month,
            'tmax': self.tmax,
            'tmaxIsEstimated': self.tmax_is_estimated,
            'tmin': self.tmin,
            'tminIsEstimated': self.tmin_is_estimated,
            'af': self.af,
            'afIsEstimated': self.af_is_estimated,
            'rain': self.rain,
            'rainIsEstimated': self.rain_is_estimated,
            'sun': self.sun,
            'sunIsEstimated': self.sun_is_estimated,
            'sunInstrument': self.sun_instrument,
            'isProvisional': self.is_provisional
        }

        if self._station_name:
            data['station'] = self.station_name()

        return json.dumps(data)
