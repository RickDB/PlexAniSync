# flake8: noqa
# pylint: skip-file
import configparser

from plexanisync.graphql import GraphQL

config = '''
[ANILIST]
username = plexanisynctest
access_token = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQ2MTQwYTkzN2JhNjIyODA2NmYyNTdmM2JiMDJiOWZmNWQ1OTgzZGVjMTdmNGRlM2RiOWEwZTM4YWQwN2Y1ODkyY2YyZjJmNjM0NjAwNTBlIn0.eyJhdWQiOiIxNTQ5IiwianRpIjoiNDYxNDBhOTM3YmE2MjI4MDY2ZjI1N2YzYmIwMmI5ZmY1ZDU5ODNkZWMxN2Y0ZGUzZGI5YTBlMzhhZDA3ZjU4OTJjZjJmMmY2MzQ2MDA1MGUiLCJpYXQiOjE3NDc2MzAxNjcsIm5iZiI6MTc0NzYzMDE2NywiZXhwIjoxNzc5MTY2MTY3LCJzdWIiOiI2MjA0NTY1Iiwic2NvcGVzIjpbXX0.OnW5RTdfMWpMBXZzY1-BGelKGBEaEiMVoImc-96Hlps_hldTWYt3puAkSpQqWSOv0ldL29BO9EkJ2615VYRgz7xWdU0ymMUIHs3slKX8UCYMzwZjmsvyzqXI_J7_md-wVc7CnotcSUl1rPGXD-cJdyS1DFDDGCuzyhnN_BS_znNQaTkSvrKu8e6hVeuj9ZwVw3I3xEDn6Z927qzTeK6U1O2V2lSGm5T0gJHW_Fnw4Khy5NrUKk-zFrgBQmHH7Q9czntLjsCkYs7AsdoXZpo7hT39KhcLoliO5Z5EkVJxRogTJmrcGWS35XzxhWMi6s8hjAxpUxW4VVDCWBplKZ68Qcf1hg8Hf5pizWz0VKJzfKZodc_Y_zzSNnTUo_aV3sOvq8TRzG64C36B9giYo2bCI7RFSgZSikUR0adTOUlksD5sCLWR3dbnDkxjMwTsekXs8LONE0pV-R7h52MTpfmyX1uvZ2S45AyRMfpfVitdM-3S0OpiFIZsmQkDZ8dvxKd0fm9zkBC9h6_Bq1bKivTHSDytrIbdjadbn8ToSXTeDp_BLYoxw4RyhXw3tkNWpoY_QF2aT_c97wEstvmWAsWG4Ij3OEYh0YONAlgSAZ94DfyDe3d2a9oxuHqtNzcqN2B8_V1Qi0DKwknBe0pgFBbuqYkiysD1RuqFgUfBnvQqVYE
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
