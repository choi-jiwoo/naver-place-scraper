# SNS text scraper

네이버 플레이스에 게시된 업체의 리뷰 데이터들를 추출해 주는 봇.

## Installation

```shell
$ pip install naverplacescraper
```

## Usage

사용 예제 [notebook](https://github.com/choi-jiwoo/naver-place-scraper) 참고.

### Naver place

네이버 플레이스에 등록된 업체들의 description 데이터과 review 데이터를 추출.

#### Quick start

[네이버 지도](map.naver.com)에서 첫번째 검색결과로 검색되는 업체의 데이터를 가져옴. 그렇기 때문에 검색결과에 따라 원하는 업체의 데이터가 뽑히지 않을 수 있음.

```python
from naverplacescraper import NaverPlace

store = NaverPlace('<store name>')
description = store.get_description()
reviews = store.get_reviews()  # defaults to 100 reviews.
```

#### Output

```
description: str

'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

reviews: pandas.DataFrame

| author | review |
|--------|--------|
|   xxxx | xxxxxx |
```

## Credit

좌표를 설정하는데 사용된 [kor_coordinates.txt](https://github.com/choi-jiwoo/naver-place-scraper/blob/master/data/kor_coordinates.txt)는 [cubensys](https://github.com/cubensys)님의 [Korea_District](https://github.com/cubensys/Korea_District)에 있는 [대한민국\_기초자치단체\_중심점\_2017.csv](https://github.com/cubensys/Korea_District/blob/master/2_%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD_%EA%B8%B0%EC%B4%88%EC%9E%90%EC%B9%98%EB%8B%A8%EC%B2%B4/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD_%EA%B8%B0%EC%B4%88%EC%9E%90%EC%B9%98%EB%8B%A8%EC%B2%B4_%EC%A4%91%EC%8B%AC%EC%A0%90_2017.csv)를 사용하였습니다.

## Disclaimer

이 프로젝트는 비상업적 용도를 위해 제작되었습니다. 용도에 맞게 사용해주시길 바랍니다.
