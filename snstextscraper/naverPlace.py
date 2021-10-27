# TO DO: Divide each flows by its functionality.
#        Remove duplicated code when making http request.
from snstextscraper.httprequest import HttpRequest
import pandas as pd


# default latitude and longitude used when opening map.
BASE_LAT = 37.278039
BASE_LONG = 127.0397669


class Store:

    def __init__(self, store_name: str) -> None:
        self.store_name = store_name
        self.id = self.get_id()
        self.description = self.get_description()
        self.reviews = self.get_reviews()

    def get_id(self) -> str:
        url = ('https://map.naver.com/v5/api/instantSearch?'
               'lang=ko&caller=pcweb&types=place,address,bus&'
               f'coords={BASE_LAT},{BASE_LONG}&query={self.store_name}')
        data = HttpRequest(url).data
        id = data['place'][0]['id']
        distance = data['place'][0]['dist']  # might be used in the future

        return id

    def get_description(self) -> str:
        url = f'https://map.naver.com/v5/api/sites/summary/{self.id}?lang=ko'
        data = HttpRequest(url).data
        description = data['description']
        keywords = data['keywords']  # might be used in the future

        return description

    def get_reviews(self) -> pd.DataFrame:
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
                    'display': 100,
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
        reviews = data['data']['visitorReviews']['items']

        return reviews
