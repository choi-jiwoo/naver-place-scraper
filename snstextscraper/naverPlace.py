from snstextscraper.httprequest import HttpRequest
import pandas as pd


# default latitude and longitude used when opening map.
BASE_LAT = 33.3789412
BASE_LONG = 126.5618716


class Search:

    def __init__(self, store_name: str, location: str = '서울') -> None:
        self.store_name = store_name
        self.location = location

    def get_search_result(self) -> str:
        url = ('https://map.naver.com/v5/api/search?caller=pcweb&'
               f'query={self.store_name}&type=all&'
               f'searchCoord={BASE_LONG};{BASE_LAT}&page=1&displayCount=20&'
               'isPlaceRecommendationReplace=true&lang=ko')

        data = HttpRequest(url).data

        try:
            search_result = data['result']['place']['list']
            candidate = pd.DataFrame(search_result)
            result_by_loc = candidate['roadAddress'].str.contains(self.location)
            most_relevant = candidate[result_by_loc].iloc[0]
            info = {
                'search_results': candidate[result_by_loc],
                'most_relevant': most_relevant,
            }
            return info
        except TypeError:
            print('조건에 맞는 업체가 없습니다.')


class Store:

    def __init__(self, id: str) -> None:
        self.id = id

    def get_description(self) -> str:
        url = f'https://map.naver.com/v5/api/sites/summary/{self.id}?lang=ko'
        data = HttpRequest(url).data
        description = data['description']
        keywords = data['keywords']  # might be used in the future

        return description

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
        data = HttpRequest(url, 'post', payload).data
        review_meta = data['data']['visitorReviews']['items']
        reviews = []

        for x in review_meta:
            review = {
                'author': x['author']['nickname'],
                'review': x['body'],
            }
            reviews.append(review)

        reviews = pd.DataFrame(reviews)

        return reviews
