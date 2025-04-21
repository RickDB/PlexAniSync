# flake8: noqa
# pylint: skip-file
import configparser

from plexanisync.graphql import GraphQL

config = '''
[ANILIST]
username = plexanisynctest
access_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImZlM2RkZjM4OGQyODE3MjY1YjIyODEzNTZkOTdjODZlMDE0ODRhYTUxZDFmMjE0ZmI5OTc0ZTZkYzUyODgxOTA5ODlmYmI0N2MzNjdlNjM4In0.eyJhdWQiOiIxNTQ5IiwianRpIjoiZmUzZGRmMzg4ZDI4MTcyNjViMjI4MTM1NmQ5N2M4NmUwMTQ4NGFhNTFkMWYyMTRmYjk5NzRlNmRjNTI4ODE5MDk4OWZiYjQ3YzM2N2U2MzgiLCJpYXQiOjE3NDUyNzc3NzksIm5iZiI6MTc0NTI3Nzc3OSwiZXhwIjoxNzc2ODEzNzc5LCJzdWIiOiI2MjA0NTY1Iiwic2NvcGVzIjpbXX0.BwCOzkRPe_Kj--MZxRqa4JJsrlHdnSYo3nvOjaB_t7PsEv5DjDOgyf9PJOZR_0eSgBLbKiY2X--XuOdZC5Hbi6izvZzwjcSyQ5ZYNAFCRnSdpiN6S3vTOa-D9kpkhxzRUSg31sLmoB4B64oYXLSSjIfer2jNpAf9tuVJVHBgDqkXdaZvgQfmR4fHZCeS1UtjCjXxm2Y7l5EY_mLZbxp_ls8HsC4IPfY8YUgD_yI2kh8LLYwXZSljPwzD8cSwj_NnAcJawzS8fbPiSj8en9iHtkYfLUXwk0LtvXivUtVDN2UL6y3MrlX1u_19Zwx2m9kJ-V9eFZiz7Eaew65Td161FQWIQVrP14Iy0GooUvtgXrES9ICjDFwSzT10I09sCDfjEqv4O1vurnWam0SQ0XLxaaSk0Yu3_tvUJ6emrYuM4AAmoQhSsf2F7gk6pxn-cfDIG3C089FyEUTPBXn661iIYiGHH7mXPP9LOZ7PyFodB6iGWEoN3TKsi4KPOkXgSXV3rEdplZPOEpf_GtMlw78xjRja49sb1iRGlf212fygEhgM9nezG6RoBIzZaqCRpURonq3nU_Ui4pzU6ccTT-5SalwNQxZfDhsdUBBauLVJyqFndjwMGJMMDKbP5kxgNQfP4-9QG9CIIdD0q6BwxHUIKIe9H0MbumRjNQR_UUAGrfQ
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
