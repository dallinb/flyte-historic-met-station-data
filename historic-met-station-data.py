#!/usr/bin/env python
"""
Extract the historical station data from the Met Office and export to various file formats.

Initially the data is exported to an Avro file.  In turn, this file is extracted to Parquet and CSV.
"""
import csv
import datetime
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import tempfile
import typing
import yaml

from fastavro import writer, parse_schema, reader
from flytekit import task, workflow
from historical.avsc import OBSERVATION_AVRO_SCHEMA
from historical.station import Station
from historical.utils import command_line_interface
from historical.utils import get_logger

if 'TMPDIR' in os.environ:
    TMPDIR = os.environ['TMPDIR']
else:
    TMPDIR = tempfile.gettempdir()


@task
def generate_avro_file(temporary_directory: str, log_level: str = 'WARN') -> str:
    """
    Extract the data from the Met Office website and write it to an Avro file.

    Parameters
    ----------
    temporary_directory : str
        The path to the temporary directory.
    log_level : str
        The log level for logging.

    Returns
    -------
    str
        The name of the Avro file generated.
    """
    today = datetime.datetime.now()
    avro_file_name = f'{temporary_directory}{os.sep}historic-station-data-{today.year}-{today.month}-{today.day}.avro'
    logger = get_logger('avro-generator', log_level)
    logger.debug(f'Avro file name is {avro_file_name}.')
    parsed_schema = parse_schema(OBSERVATION_AVRO_SCHEMA)
    total_records_written = 0

    with open('stations.yml') as stream:
        stations_data = yaml.safe_load(stream)['stations']

    # Write the initial schema to the Avro file.
    avro_file = open(avro_file_name, 'wb')
    writer(avro_file, parsed_schema, [])

    # New reopen the file to write the data to it.
    avro_file.close()
    avro_file = open(avro_file_name, 'a+b')

    for station in stations_data:
        logger.debug(station)
        station = Station(station['name'], station['url'], log_level)
        observations = station.get_observations()
        observation_count = 0

        for observation in observations:
            observation.station_name(station.name)
            logger.debug(observation)

            if not observation_count:
                start_date = f'{observation.year}-{observation.month:02}'

            observation_count += 1
            total_records_written += 1
            writer(avro_file, parsed_schema, [observation.to_dict()])

        end_date = f'{observation.year}-{observation.month:02}'
        logger.info(
            f'Gathered {observation_count:,} observations from {station.name} between {start_date} and {end_date:02}.'
        )

    avro_file.close()
    logger.info(f'Wrote {total_records_written:,} to {avro_file_name}.')
    return avro_file_name


@task
def generate_csv_file(avro_file_name: str, log_level: str = 'WARN') -> str:
    """
    Generate a CSV file from an Avro file.

    Parameters
    ----------
    avro_file_name : str
        The full path to the Avro file.
    log_level : str, optional
        The log level (e.g. INFO), by default 'WARN'.

    Returns
    -------
    str
        The full path to the CSV file.
    """
    csv_file_name = avro_file_name.replace('.avro', '.csv')
    logger = get_logger('csv-generator', log_level)
    record_count = 0
    fieldnames = []

    with open(avro_file_name, 'rb') as avro_file_stream:
        avro_reader = reader(avro_file_stream)
        schema = avro_reader.writer_schema

        for field in schema['fields']:
            fieldnames.append(field['name'])

        logger.debug(f'Schema fieldnames are {",".join(fieldnames)}.')

        with open(csv_file_name, 'w') as csv_file_stream:
            csv_writer = csv.DictWriter(csv_file_stream, fieldnames=fieldnames)
            csv_writer.writeheader()

            for record in avro_reader:
                record_count += 1
                csv_writer.writerow(record)

    logger.info(f'Wrote {record_count:,} to {csv_file_name}.')
    return csv_file_name


@task
def generate_parquet_file(avro_file_name: str, log_level: str = 'WARN') -> str:
    """
    Create a Parquet file from an Avro file.

    Parameters
    ----------
    avro_file_name : str
        The full path to the Avro file.
    log_level : str, optional
        The log level (e.g. INFO), by default 'WARN'.

    Returns
    -------
    str
        The full path to the Parquet file.
    """
    parquet_file_name = avro_file_name.replace('.avro', '.parquet')
    logger = get_logger('parquet-generator', log_level)

    with open(avro_file_name, 'rb') as avro_file_stream:
        avro_reader = reader(avro_file_stream)
        df = pd.DataFrame.from_records(avro_reader)

    record_count = len(df)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_file_name)
    logger.info(f'Wrote {record_count:,} records to {parquet_file_name}.')
    return parquet_file_name


@workflow
def wf(temporary_directory: str, log_level: str = 'WARN') -> typing.Tuple[str, str, str]:
    """
    Extract and conversion of the historical data via a Flyte workflow.

    Parameters
    ----------
    temporary_directory : str
        The path to the temporary directory.
    log_level : str, optional
        The log level for logging.  Default value is 'WARN'.

    Returns
    -------
    Tuple[str, str, str]
        A tuple containing the name of the Avro file, Parquet file and CSV file.
    """
    avro_file_name = generate_avro_file(temporary_directory=temporary_directory, log_level=log_level)
    parquet_file_name = generate_parquet_file(avro_file_name=avro_file_name, log_level=log_level)
    csv_file_name = generate_csv_file(avro_file_name=avro_file_name, log_level=log_level)
    return (avro_file_name, parquet_file_name, csv_file_name)


if __name__ == '__main__':
    args = command_line_interface()

    if args.verbose:
        log_level = 'INFO'
    elif args.debug:
        log_level = 'DEBUG'
    else:
        log_level = 'WARN'

    wf(temporary_directory=TMPDIR, log_level=log_level)
