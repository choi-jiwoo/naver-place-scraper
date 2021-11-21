"""This module scrapes review data of a store from Naver Place."""
import pandas as pd
from naverplacescraper.coordinates import get_coordinates
from naverplacescraper.httprequest import HttpRequest


class Store:
    """A class representing a store.

    :param store: Store name or id.
    :type store: str
    :param location: Default location to search, defaults to '서울'
    :type location: str, optional
    :param by_id: Search with a store ID, defaults to False.
    :type by_id: bool, optional
    """

    def __init__(self, store: str, location: str = '서울',
                 by_id: bool = False) -> None:
        self.store = store
        self.location = location

        if by_id:
            self.id = store
        else:
            self.info = self.get_search_result()
            self.id = self._get_id()

    def get_search_result(self) -> dict:
        """Get search result of a store in naver place.

        :return: Both search results and top search result.
        :rtype: dict
        """
        longitude, latitude = get_coordinates(self.location)
        url = ('https://map.naver.com/v5/api/search?caller=pcweb&'
               f'query={self.store}&type=all&'
               f'searchCoord={longitude};{latitude}&page=1&displayCount=10&'
               'isPlaceRecommendationReplace=true&lang=ko')

        data = HttpRequest(url).data

        try:
            search_result = data['result']['place']['list']
            candidate = pd.DataFrame(search_result)

            pattern = f'[{self.location}]'
            result_by_loc = candidate['roadAddress'].str.contains(pattern)
            search_results = candidate[result_by_loc]
            most_relevant = search_results.iloc[0]
            info = {
                'search_results': search_results,
                'most_relevant': most_relevant,
            }

            return info
        except (TypeError, IndexError, KeyError):
            print('검색 결과가 없습니다.')
            return

    def _get_id(self) -> str:
        if self.info is None:
            return
        most_relevant = self.info['most_relevant']
        store_id = most_relevant['id']

        return store_id

    def get_description(self) -> str:
        try:
            url = f'https://map.naver.com/v5/api/sites/summary/{self.id}?lang=ko'
            data = HttpRequest(url).data
            description = data['description']
            keywords = data['keywords']  # might be used in the future

            return description
        except KeyError:
            return

    def get_reviews(self, num_of_reviews: int = 100) -> dict:
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
                    'businessId': self.id,
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
                'id': self.id,
            },
            'query': query
        }
        try:
            data = HttpRequest(url, 'post', payload).data
            review_meta = data['data']['visitorReviews']['items']
            reviews = []

            for x in review_meta:
                review = {
                    'author': x['author']['nickname'],
                    'rating': x['rating'],
                    'review': x['body'],
                }
                reviews.append(review)

            reviews = pd.DataFrame(reviews, columns=['author', 'rating', 'review'])

            return reviews
        except (TypeError, KeyError):
            return
