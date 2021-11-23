"""This module gets longitude and latitude of certain places in South Korea"""
import pandas as pd
from importlib import resources
from importlib_resources import files
import data


def get_coordinates(location: str) -> tuple:
        """Get coordinates of a given region.

        :return: Longitude and latitude value of a region.
        :rtype: tuple
        """
        path_to_file = files(data).joinpath('kor_coordinates.txt')
        coordinates = pd.read_csv(path_to_file, delimiter=',', encoding='euc-kr')
        coordinates['X'] = coordinates['X'].round(7)
        coordinates['Y'] = coordinates['Y'].round(7)

        pattern = f'({location}?)'
        _ = coordinates['SIG_KOR_NM'].str.extract(pattern)
        _ = _.fillna('')
        most_relevant = coordinates.iloc[_[0].map(len).idxmax()]
        longitude = most_relevant['X']
        latitude = most_relevant['Y']

        return (longitude, latitude)