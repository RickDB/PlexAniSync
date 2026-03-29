# flake8: noqa
# pylint: skip-file
import configparser

from plexanisync.graphql import GraphQL

config = '''
[ANILIST]
username = plexanisynctest
access_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJlZGFhYTNjZjFmOTI3Mjc2ZDg1MWI1MjcxODNjZjFmOTJlYjYzNzBlMGMzZmE1NDYyNWMzMWYwMzgyNjI3MGNjMjRmMThmNmQ4NzM4MmI5In0.eyJhdWQiOiIxNTQ5IiwianRpIjoiMmVkYWFhM2NmMWY5MjcyNzZkODUxYjUyNzE4M2NmMWY5MmViNjM3MGUwYzNmYTU0NjI1YzMxZjAzODI2MjcwY2MyNGYxOGY2ZDg3MzgyYjkiLCJpYXQiOjE3NzQ4MDg0MDQsIm5iZiI6MTc3NDgwODQwNCwiZXhwIjoxODA2MzQ0NDA0LCJzdWIiOiI2MjA0NTY1Iiwic2NvcGVzIjpbXX0.GkkWK5xu_XvE4dj_tCHL58iK0Tl__cV-2B59KZMJ_pGEaWhT0vcvKyB25wQ8Nb7ItfJZFG_M2IPBxkXdq33k-0YYC-Fqd7bT1PLf8WjXLG5iDrG0u9ld7G7k8A2geQM10mnikVS5UgQcHCQ0mc77xWq7YevrqsTzLOQ_Dl0C-nWZ0iWqzfkaYzMo7XQ7Ru4W2Pe-uN19bDnC28F7f3BG37bP_ZDhXmw8yKpImAn8hAS-Risxfxgsrr0MGApvNF2Ebucz36Dggkha0D-wMT4wib58JFkUaAHoavX-0Hh33GBCvSy4gw-cYVyg8zEVMZ67Tszs5ZS6RUvXQ5lkzSRLmwvKiETj13CUhQFUoTpXGBBGs4XJ6jOeGYQEWd0Kzk0Dre3cwx84oqy4CjnjFEbzRLs8vxkBLMtvuBaRo_v_iynQuwAMsNTArB5hPrx-cuMTKt1eKRhSbVs4Xjst_h45sul7QA4p-QIdQEZvu3xNoBIw4kizeTpD4XN7Yrohbr4ehNBQNbzOkkLh9RKYGvTo5V6OtAksNerys83OCDhxqZRODU-QwDm85tan5Q12FYm-cw7n9kh8B37-GU_7jSuPZojUnLeXPj18DfpGX8Ajy48dCCB9tLvCAMRftoydn_RCHtxTeUSp0hz_zjPY1DJN2qRHv3al4FYmUvDCnl_hvSw
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
