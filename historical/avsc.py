"""avsc.py."""


OBSERVATION_AVRO_SCHEMA = {
    'type': 'record',
    'name': 'MonthlyHistoricalObservation',
    'doc': 'A monthly observation from a station of the Historic Station Data.  See <https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data>.',
    'namespace': 'uk.gov.metoffice',
    'fields': [
        {
            'name': 'station',
            'type': 'string',
            'doc': 'The name of the station the observation is for (e.g. Ross-on-Wye).'
        },
        {
            'name': 'year',
            'type': 'int',
            'doc': 'The year the observation took place.'
        },
        {
            'name': 'month',
            'type': 'int',
            'doc': 'The month within the specified year that the observation took place.'
        },
        {
            'name': 'tmax',
            'type': [
                'double',
                'null'
            ],
            'doc': 'Mean daily maximum temperature for the observation (degC).  Set to null if two or more days are missing in the month.'
        },
        {
            'name': 'tmaxIsEstimated',
            'type': 'boolean',
            'doc': 'Was tmax estimated for this month.'
        },
        {
            'name': 'tmin',
            'type': [
                'double',
                'null'
            ],
            'doc': 'Mean daily minimum temperature for the observation (degC).  Set to null if two or more days are missing in the month.'
        },
        {
            'name': 'tminIsEstimated',
            'type': 'boolean',
            'doc': 'Was tmin estimated for this month.'
        },
        {
            'name': 'af',
            'type': [
                'int',
                'null'
            ],
            'doc': 'Days of air frost.  Set to null if two or more days are missing in the month.'
        },
        {
            'name': 'afIsEstimated',
            'type': 'boolean',
            'doc': 'Was af estimated for this month.'
        },
        {
            'name': 'rain',
            'type': [
                'double',
                'null'
            ],
            'doc': 'Total rain fall for the observation (mm).  Set to null if two or more days are missing in the month.'
        },
        {
            'name': 'rainIsEstimated',
            'type': 'boolean',
            'doc': 'Was rain estimated for this month.'
        },
        {
            'name': 'sun',
            'type': [
                'double',
                'null'
            ],
            'doc': 'Total sun duration for the observation (hours).  Set to null if two or more days are missing in the month.'
        },
        {
            'name': 'sunIsEstimated',
            'type': 'boolean',
            'doc': 'Was sun estimated for this month.'
        },
        {
            'name': 'sunInstrument',
            'type': [
                'string',
                'null'
            ],
            'doc': 'The instrument type (if known) to measure the hours of sun duration.  Will either be Kipp & Zonen or Campbell Stokes.'
        },
        {
            'name': 'isProvisional',
            'type': 'boolean',
            'doc': 'Data is provisional until the full network quality control has been carried out.'
        }
    ]
}
