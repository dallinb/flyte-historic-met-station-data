Feature: Met Office Historical Station Data
    Scenario Outline: Observation Parsing
        Given input line is <line>

        When line is parsed

        Then year is <year>
        And month is <month>
        And tmax is <tmax>
        And tmax_is_estimated is <tmax_is_estimated>
        And tmin is <tmin>
        And tmin_is_estimated is <tmin_is_estimated>
        And af is <af>
        And af_is_estimated is <af_is_estimated>
        And rain is <rain>
        And rain_is_estimated is <rain_is_estimated>
        And sun is <sun>
        And sun_is_estimated <sun_is_estimated>
        And sun_instrument is <sun_instrument>
        And is_provisional is <is_provisional>

        Examples:
        | line                                    | year | month | tmax | tmax_is_estimated | tmin | tmin_is_estimated | af   | af_is_estimated | rain | rain_is_estimated | sun   | sun_is_estimated | sun_instrument  | is_provisional |
        | 1941 1 --- --- --- 74.7 ---             | 1941 | 1     | ---  | False             | ---  | False             | ---  | False           | 74.7 | False             | ---   | False            | ---             | False          |
        | 1957 1 8.6 3.9 2 80.6 55.6              | 1957 | 1     | 8.6  | False             | 3.9  | False             | 2    | False           | 80.6 | False             | 55.6  | False            | Campbell Stokes | False          |
        | 1945 3 11.8 4.1 1 35.8                  | 1945 | 3     | 11.8 | False             | 4.1  | False             | 1    | False           | 35.8 | False             | ---   | False            | ---             | False          |
        | 2001 5 15.4 8.6 0 44.4 236.8*           | 2001 | 5     | 15.4 | False             | 8.6  | False             | 0    | False           | 44.4 | Falsse            | 236.8 | True             | ---             | False          |
        | 2022 1 8.6 4.1 1 32.2 56.3# Provisional | 2022 | 1     | 8.6  | False             | 4.1  | False             | 1    | False           | 32.2 | False             | 56.3  | False            | Kipp & Zonen    | True           |
