# SNS text scraper

네이버 플레이스와 인스타그램에 게시된 업체의 관한 텍스트 데이터들을 추출해 줌.

### Naver place

네이버 플레이스에 등록된 업체들의 description 데이터과 review 데이터를 추출.

#### Quick start

```python
from snstextscraper.naverplace import Store

store = Store('<store name>')

id = store.id
description = store.description
reviews = store.reviews  # dictionary in {author: review} form
```

### Instagram

인스타그램에서 검색 결과로 나온 게시물들의 게시글을 추출.

#### Quick start

```python
from snstextscraper.driver import Driver
from snstextscraper.instagram import Instagram

driver = Driver('<path to chromedriver>')
driver = driver.driver()

insta = Instagram(driver)
insta.login('<username>', '<password>')
insta.search('<store name>')
post = insta.get_contents() # dictionary in {author: post} form
insta.next_post()

insta.driver.quit()  # if headless option in Driver is False
```
