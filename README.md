# SNS text scraper

네이버 플레이스와 인스타그램에 게시된 업체의 관한 텍스트 데이터들을 추출해 주는 봇.

## Installation

```shell
$ pip install snstextscraper
```

## Usage

### Naver place

네이버 플레이스에 등록된 업체들의 description 데이터과 review 데이터를 추출.

#### Quick start

```python
from snstextscraper.naverplace import Store

store = Store('<store name>')

description = store.description
reviews = store.reviews
```

#### Output

```
reviews:

| author | review |
|--------|--------|
|   xxxx | xxxxxx |
```

### Instagram

인스타그램에서 검색 결과로 나온 게시물들의 caption을 추출. (⚠️ 한글 사이트에서만 작동함)

#### Quick start

```python
from snstextscraper.driver import Driver
from snstextscraper.instagram import Instagram
import time
import pandas as pd

driver = Driver('<path to chromedriver>', headless=False)
driver = driver.driver()

insta = Instagram(driver)
insta.login('<username>', '<password>')
insta.search('<store name>')

posts = []
num_of_posts = 5

for i in range(num_of_posts):
    post = insta.get_contents()  # dictionary in {'author': author, 'caption': caption}
    posts.append(post)
    insta.next_post()
    time.sleep(5)  # be gentle in scraping data. Instagram might ban your account.

posts = pd.DataFrame(posts)

# if driver is in headless mode
insta.driver.quit()
# else
insta.driver.close()
```

#### Output

```
posts:

| author | caption |
|--------|---------|
|   xxxx |  xxxxxx |
```

## Disclaimer

이 프로젝트는 비상업적 용도를 위해 제작되었습니다. 용도에 맞게 사용해주시길 바랍니다.

또한 인스타그램은 데이터 보안 정책상 공식적으로 봇을 사용한 크롤링을 하지 못하게 일정량 리밋을 걸거나 봇으로 의심되는 계정을 정지시키기도 합니다. 인스타그램 데이터를 크롤링할 땐 부계정 사용을 권장하고, 발생할 수 있는 불이익들을 생각해보고 진행하시길 바랍니다. 본인 책임 하에 사용바라며, 사용 중 발생하는 모든 불이익들에 대해 제작자는 책임이 없음을 알려드립니다. (가장 좋은 방법은 [인스타그램 API](https://developers.facebook.com/docs/instagram)를 사용하는 것)

