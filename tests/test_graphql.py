# flake8: noqa
# pylint: skip-file
import configparser

from plexanisync.graphql import GraphQL

config = '''
[ANILIST]
username = plexanisynctest
access_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjkzOTJiNzBjMWJlMzRjNzhlYjQ4MGQ5Y2JjYTI5Y2I2NmQyMjc5MmFlZGRjNzJjN2EzMzRjMTZhOWMwMTA2N2U3ZWMwYTc0M2ZhNzRkNTgxIn0.eyJhdWQiOiIxNTQ5IiwianRpIjoiOTM5MmI3MGMxYmUzNGM3OGViNDgwZDljYmNhMjljYjY2ZDIyNzkyYWVkZGM3MmM3YTMzNGMxNmE5YzAxMDY3ZTdlYzBhNzQzZmE3NGQ1ODEiLCJpYXQiOjE3MTExNDc1MTQsIm5iZiI6MTcxMTE0NzUxNCwiZXhwIjoxNzQyNjgzNTE0LCJzdWIiOiI2MjA0NTY1Iiwic2NvcGVzIjpbXX0.nE-FWBzuWfbUMdpeEqr1wbYem3VDm4KHXs1VYGAclF8b8PTfMv60_gH7sTEVklQ5sVnW7Gy4wMoFhH5KcbyOyNlWpw2R2qn2NYL2lvOy4fOLkS2AR48UY1_tQuYbIE55ZjaIYIODrp6tb7Vk8mEEgC2sN_jvQAK10nMfRd1IlGRLU41B9bDsiv8QebVEyQJWR2cQ3QMOqXG2HQNdQgZLCnJZABZxx66dNzk_XBDLWaNtxPAd4Co9K0Vi87KatvQgzMi30zFlkdowl8R_1qr0CkySnw4bIjcUfk1rPKdgoUSdq_o9WZfsNhYgAomgE_HKQiZY_d1QU6WCiv99gh5yh6R2fCgcKfs-jmwgVvCleAiI4qFKy6WSqrwEvYPYZhiEJ_mybyUc9fHAN-v9Z1TGHMjg3pbBFv6TvCvxJYm3CATndxRzxe6nDHedxF6occpO90CUgc80JNP25jWfN9ObpJ7qbZwFoY9GF3-vkshd1trY6ghZx02vlsyfBuTFIz-UaTB0uw5uBYVWUiQ9-qyT0Ghi1L3_y2nVctVoUdD_WonxQcOm1ycE3HQDYuci8xcij3g-NASpE72VSV0XUjMwPfXcGzWmM9BdFBLe1juQDalUS4Sab2waThd_NXC3Wu6vWjJmzT-xVtjS7pOQmyfXVHnpjUOLuoGEVjetgHPy7GY
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
