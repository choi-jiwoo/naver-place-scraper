import pandas as pd
from snstextscraper.httprequest import HttpRequest


# default latitude and longitude used when opening map.
BASE_LAT = 33.3789412
BASE_LONG = 126.5618716


class Search:

    def __init__(self, store: str, location: str = '서울') -> None:
        self.store = store
        self.location = location

    def get_search_result(self) -> str:
        url = ('https://map.naver.com/v5/api/search?caller=pcweb&'
               f'query={self.store}&type=all&'
               f'searchCoord={BASE_LONG};{BASE_LAT}&page=1&displayCount=10&'
               'isPlaceRecommendationReplace=true&lang=ko')

        data = HttpRequest(url).data

        try:
            search_result = data['result']['place']['list']
            candidate = pd.DataFrame(search_result)

            return candidate
        except (TypeError, IndexError, KeyError):
            print(f'{self.store}. 조건에 맞는 업체가 없습니다.')

    def get_results_by_location(self) -> dict:
        try:
            candidate = self.get_search_result()
            pattern = f'[{self.location}]'
            result_by_loc = candidate['roadAddress'].str.contains(
                pattern,
                regex=True,
            )
            search_results = candidate[result_by_loc]
            most_relevant = search_results.iloc[0]
            info = {
                'search_results': search_results,
                'most_relevant': most_relevant,
            }

            return info
        except IndexError:
            print('지역 검색결과가 없습니다.')
            return


class Store(Search):

    def __init__(self, store: str,
                 location: str = '서울', by_id: bool = False) -> None:
        super().__init__(store, location)
        if not by_id:
            self.info = self.get_results_by_location()
            self.id = self._get_id()
        else:
            self.id = store

    def _get_id(self) -> str:
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
                    'review': x['body'],
                }
                reviews.append(review)

            reviews = pd.DataFrame(reviews, columns=['author', 'review'])

            return reviews
        except KeyError:
            return
