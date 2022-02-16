"""This module retrieves search results from Naver place."""
from typing import Optional
import pandas as pd
from naverplacescraper.coordinates import get_coordinates
from naverplacescraper.utils import empty_result
from naverplacescraper.httprequest import Get
from naverplacescraper.httprequest import Post


class NaverPlace:
    """A class representing a store registered in Naver place.

    :param store: Store name or ID.
    :type store: str
    :param location: Default location to search, defaults to '서울'.
    :type location: str, optional
    """
    
    #: Default headers to pass in a HTTP request.
    headers = {'User-Agent': 'Mozilla'}

    def __init__(self, store: str, location: str = '서울') -> None:
        self.store = store
        self.location = location

        self.search_result = self._get_search_result()
        self.info = self._summarize_info()
        self._id = self.info['id']
        self.raw_review_data = None
        
    def attach_headers(self, headers: dict) -> None:
        """Attach custom HTTP headers.
        
        :param headers: HTTP headers.
        :type headers: dict
        """
        self.headers = headers

    def _get_search_result(self) -> pd.DataFrame:
        """Get search result of a store in naver place.

        :return: Both search results and top search result.
        :rtype: dict
        """
        longitude, latitude = get_coordinates(self.location)
        url = ('https://map.naver.com/v5/api/search?caller=pcweb&'
               f'query={self.store}&type=all&'
               f'searchCoord={longitude};{latitude}&page=1&displayCount=10&'
               'isPlaceRecommendationReplace=true&lang=ko')

        get = Get(url, self.headers)
        data = get.request()

        try:
            search_result = data['result']['place']['list']
            candidate = pd.DataFrame(search_result)

            pattern = f'[{self.location}]'
            result_by_loc = candidate['roadAddress'].str.contains(pattern)
            search_results = candidate[result_by_loc]

            if search_results.empty:
                empty_result()
                return

            return search_results
        except (TypeError, IndexError, KeyError):
            empty_result(f'[{self.store}]에 대한 검색 결과가 존재하지 않습니다.')
            return

    def _summarize_info(self) -> pd.Series:
        """Get summarized information of the first search result.

        :return: Summarized store info
        :rtype: pd.Series
        """
        first = self.search_result.iloc[0]
        info_list = [
            'id',
            'name',
            'tel',
            'roadAddress',
            'reviewCount',
            'bizhourInfo',
            'x',
            'y',
        ]
        info = first[info_list]

        return info

    def get_description(self) -> str:
        """Get a store description.

        :return: A store description. `None` is returned when the
            result is empty.
        :rtype: str
        """
        url = f'https://map.naver.com/v5/api/sites/summary/{self._id}?lang=ko'
        try:
            get = Get(url, self.headers)
            data = get.request()
            description = data['description']
            keywords = data['keywords']  # might be used in the future

            return description
        except KeyError:
            empty_result()
            return

    def _get_raw_reviews(self, num_of_reviews: int) -> None:
        """Get a raw user review data of a store.

        :param num_of_reviews: Maximum number of reviews to get.
        :type num_of_reviews: int
        """
        url = 'https://api.place.naver.com/graphql'
        # grapql query
        query = ('query getVisitorReviews($input: VisitorReviewsInput) {'
                 '\n  visitorReviews(input: $input) {'
                 '\n    items {'
                 '\n      id'
                 '\n      rating'
                 '\n      author {'
                 '\n        id'
                 '\n        nickname'
                 '\n        from'
                 '\n        imageUrl'
                 '\n        objectId'
                 '\n        url'
                 '\n        review {'
                 '\n          totalCount'
                 '\n          imageCount'
                 '\n          avgRating'
                 '\n          __typename'
                 '\n        }'
                 '\n        __typename'
                 '\n      }'
                 '\n      body'
                 '\n      thumbnail'
                 '\n      media {'
                 '\n        type'
                 '\n        thumbnail'
                 '\n        __typename'
                 '\n      }'
                 '\n      tags'
                 '\n      status'
                 '\n      visitCount'
                 '\n      viewCount'
                 '\n      visited'
                 '\n      created'
                 '\n      reply {'
                 '\n        editUrl'
                 '\n        body'
                 '\n        editedBy'
                 '\n        created'
                 '\n        replyTitle'
                 '\n        __typename'
                 '\n      }'
                 '\n      originType'
                 '\n      item {'
                 '\n        name'
                 '\n        code'
                 '\n        options'
                 '\n        __typename'
                 '\n      }'
                 '\n      language'
                 '\n      highlightOffsets'
                 '\n      translatedText'
                 '\n      businessName'
                 '\n      showBookingItemName'
                 '\n      showBookingItemOptions'
                 '\n      bookingItemName'
                 '\n      bookingItemOptions'
                 '\n      __typename'
                 '\n    }'
                 '\n    starDistribution {'
                 '\n      score'
                 '\n      count'
                 '\n      __typename'
                 '\n    }'
                 '\n    hideProductSelectBox'
                 '\n    total'
                 '\n    __typename'
                 '\n  }'
                 '\n}'
                 '\n')

        payload = {
            'operationName': 'getVisitorReviews',
            'variables': {
                'input': {
                    'businessId': self._id,
                    'businessType': 'restaurant',
                    'item': '0',
                    'bookingBusinessId': None,
                    'page': 1,
                    'display': num_of_reviews,
                    'isPhotoUsed': False,
                    'theme': 'allTypes',
                    'includeContent': True,
                    'getAuthorInfo': False,
                },
                'id': self._id,
            },
            'query': query
        }
        try:
            post = Post(url, payload, self.headers)
            data = post.request()
            raw_review_data = data['data']['visitorReviews']['items']

            self.raw_review_data = raw_review_data
        except (TypeError, KeyError):
            empty_result()
            
    def get_reviews(self, num_of_reviews: int = 100) -> pd.DataFrame:
        """Extract visit date, author, and review data of a store from raw review data.

        :param num_of_reviews: Maximum number of reviews to get, defaults to 100
        :type num_of_reviews: int, optional
        :return: Review data with date, author, and reviews.
        :rtype: pd.DataFrame
        """
        self._get_raw_reviews(num_of_reviews)

        if self.raw_review_data is None:
            return

        reviews = []

        for x in self.raw_review_data:
            review = {
                'date': x['visited'],
                'author': x['author']['nickname'],
                'review': x['body'],
            }
            reviews.append(review)

        reviews = pd.DataFrame(
            reviews,
            columns=['date', 'author', 'review'],
        )

        return reviews

    def __repr__(self) -> str:
        return f'NaverPlace(store="{self.store}", location="{self.location}")'