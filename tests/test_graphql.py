# flake8: noqa
# pylint: skip-file
import configparser

from plexanisync.graphql import GraphQL

config = '''
[ANILIST]
username = plexanisynctest
access_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkwMzBlNmZiZDBhZGZkZDFhMDgxNTMwOGU5MzhlYmI0ZmUzZWU0ZThmYmVkOTFkNWU0NjBjYmUwZmFmMjNiNDg3MWM0ZDRiMGYzNTkxZWUzIn0.eyJhdWQiOiIxNTQ5IiwianRpIjoiOTAzMGU2ZmJkMGFkZmRkMWEwODE1MzA4ZTkzOGViYjRmZTNlZTRlOGZiZWQ5MWQ1ZTQ2MGNiZTBmYWYyM2I0ODcxYzRkNGIwZjM1OTFlZTMiLCJpYXQiOjE2Nzg3MzIzOTUsIm5iZiI6MTY3ODczMjM5NSwiZXhwIjoxNzEwMzU0Nzk1LCJzdWIiOiI2MjA0NTY1Iiwic2NvcGVzIjpbXX0.e3VitKC66OImoLPlKnHBbN8SQTcbj3ClIyW_bVyl9UuL_JHQ80p0stGDenJVijw-KV1Dr-ODfJggYormVcYepLX99KjJ4vjaIB1ABS7QfrBiJwhmfJpZLCFx44A4owD5kFsLfVy09YsQL2ZsX3YOr3-ItWF-cV904FZWemKEXhf9znOJ2S594HaQKTERbW518_Vd0L7JdrBDupcBkEtssz3mw8OGb4nytIkYkYL8qde3kvnUYxciun3oQASe5PabcltJoQClT2Gdalavm_BbmSygjpsMyX_j57te_8xOAvDclOGu9BYRY5j_-Db3OAUM-HwuiyKt10O3o_OmH2tzLlhSK9dHiGvgr2h52P5BfkDky3TO-RMlDXcswLwc5lXhTnpESYt9Tw7FOmP-fRuzLvyn5-E_XXFXjEtjR7rqmsaoRb5EGGq2UavG5i4y96yy1IlDHb6rCPFpMEYg3XRyi7XPJbTPsYv9x3f55cDiKgw9GsPyEFzRFQN5Uzz5ePJgDUXErtXlHvLFknI-W10hQvZIn_onpBHdjfIq6cQEWJRf8UyojuXfwBBkFbFi9XjKcDR_Z0V_q_UtE1ykjk3QRXzCDQx2IBFHkpkXWzktSZXurjVX4-XQbNCBPeyWomGrbpjavltp3tEgMO6sTamIED6GzBa6JkHgNqCU3JGa0gY
'''

settings = configparser.ConfigParser()
settings.read_string(config)
graphql = GraphQL(settings["ANILIST"])


def test_fetch_user_list():
    medialist = graphql.fetch_user_list()
    
    assert len(medialist) == 1
    naruto = medialist[0]
    assert naruto.title_english == "Naruto"
    assert naruto.status == "CURRENT"
    assert naruto.progress == 4
    assert naruto.score == 70

def test_too_many_requests(caplog):
    for i in range(200):
        graphql.fetch_user_list()
        if "Rate limit hit, waiting for" in caplog.text:
            break
    
    assert "Rate limit hit, waiting for" in caplog.text


def test_search_by_id():
    media = graphql.search_by_id(20)
    assert media
    assert media.title_english == "Naruto"

def test_search_by_name():
    search_results = graphql.search_by_name("Naruto")
    assert len(search_results) > 20
