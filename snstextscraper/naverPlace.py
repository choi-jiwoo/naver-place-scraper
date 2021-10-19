# TO DO: Divide each flows by its functionality.
import requests
import json


# flow 1: get Store Id
BASE_LAT = 37.278039
BASE_LONG = 127.0397669
query = '애플망고1947'
url = ('https://map.naver.com/v5/api/instantSearch?'
       'lang=ko&caller=pcweb&types=place,address,bus&'
       f'coords={BASE_LAT},{BASE_LONG}&query={query}')
headers = {'User-Agent': 'Mozilla'}

res = requests.get(url, headers=headers)
res.status_code
data = json.loads(res.text)

# return
_id = data['place'][0]['id']
distance = data['place'][0]['dist']

# flow 2: get Store descriptions
url = f'https://map.naver.com/v5/api/sites/summary/{_id}?lang=ko'
res = requests.get(url, headers=headers)
res.status_code
data = json.loads(res.text)

# return
description = data['description']
keywords = data['keywords']

# flow 3: get Store reviews
url = 'https://api.place.naver.com/graphql'
headers = {'User-Agent': 'Mozilla'}
_id = '1183779572'

# grapql
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
            'businessId': _id,
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
        'id': _id,
    },
    'query': query
}

res = requests.post(url, headers=headers, json=payload)
res.status_code
data = res.json()

# return
# example review no. 19
review_num = 19
print(data['data']['visitorReviews']['items'][review_num]['author']['nickname'])
print(data['data']['visitorReviews']['items'][review_num]['body'])
