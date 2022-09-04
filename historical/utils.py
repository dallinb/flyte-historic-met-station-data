"""
Utility methods.

Methods
-------
command_line_interface - Parse command line arguments.
"""
import logging
import sys

from argparse import ArgumentParser


def command_line_interface(args: list = sys.argv):
    """
    Process arguments provided by the command line.

    Parameters
    ----------
    args : list of str
        The arguments to be processed.

    Returns
    -------
    argparse.Namespace
        The command line arguments provided.
    """
    parser = ArgumentParser(args, description='Import and translate historical meteorological station data.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--debug', help='Is logging to be DEBUG level?', action='store_true')
    group.add_argument('-v', '--verbose', help='Is logging to be INFO level?', action='store_true')
    return parser.parse_args()


def get_logger(name: str, log_level=logging.WARN) -> logging.Logger:
    """
    Generate a logger in a uniform fashion.

    Parameters
    ----------
    name : str
        The name of the logger.
    log_level : str
        The logging level (e.g. 'INFO' or 'DEBUG')

    Returns
    -------
    logging.Logger
        The produced logger.
    """
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
