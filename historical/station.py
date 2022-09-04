"""station.py."""
from curses.ascii import isdigit
from historical.observation import Observation
from historical.utils import get_logger
from smart_open import open


class Station:
    """The Station class."""

    def __init__(self, name: str, url: str, log_level: str = 'WARN') -> None:
        """
        Create a Station object.

        Parameters
        ----------
        name : str
            The name of the station (e.g. Wick Airport).
        url : str
            The URL to the historical data for this station.
        log_level : str
            The log level for logging.
        """
        self.name = name
        self.url = url
        self.logger = get_logger(f'Station:{name}', log_level)

    def get_observations(self):
        """
        Get observations from the station data.

        Yields
        ------
        Observation
            The observation data.
        """
        self.logger.debug(f'Reading data from {self.url} for station {self.name}.')

        # invalid_patters = [
        #     # Patterns that are non-standard, but have made it into the data.
        #     '$',
        #     'all data from Whitby',
        #     'Change to Monckton Ave'
        # ]

        with open(self.url, 'r') as stream:
            for line in stream:
                line = line.strip()

                if len(line) == 0 or not isdigit(line[0]):
                    continue

                # for invalid_pattern in invalid_patters:
                #     line = line.replace(invalid_pattern, '')

                self.logger.debug(line)
                observation = Observation(line)
                yield observation
