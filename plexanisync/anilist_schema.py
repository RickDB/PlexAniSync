# flake8: noqa
# pylint: skip-file
# type: ignore
import sgqlc.types
import sgqlc.types.relay


anilist_schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
anilist_schema -= sgqlc.types.relay.Node
anilist_schema -= sgqlc.types.relay.PageInfo



########################################################################
# Scalars and Enumerations
########################################################################
class ActivitySort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ID', 'ID_DESC', 'PINNED')


class ActivityType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ANIME_LIST', 'MANGA_LIST', 'MEDIA_LIST', 'MESSAGE', 'TEXT')


class AiringSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('EPISODE', 'EPISODE_DESC', 'ID', 'ID_DESC', 'MEDIA_ID', 'MEDIA_ID_DESC', 'TIME', 'TIME_DESC')


Boolean = sgqlc.types.Boolean

class CharacterRole(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('BACKGROUND', 'MAIN', 'SUPPORTING')


class CharacterSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('FAVOURITES', 'FAVOURITES_DESC', 'ID', 'ID_DESC', 'RELEVANCE', 'ROLE', 'ROLE_DESC', 'SEARCH_MATCH')


class CountryCode(sgqlc.types.Scalar):
    __schema__ = anilist_schema


class ExternalLinkMediaType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ANIME', 'MANGA', 'STAFF')


class ExternalLinkType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('INFO', 'SOCIAL', 'STREAMING')


Float = sgqlc.types.Float

class FuzzyDateInt(sgqlc.types.Scalar):
    __schema__ = anilist_schema


ID = sgqlc.types.ID

Int = sgqlc.types.Int

class Json(sgqlc.types.Scalar):
    __schema__ = anilist_schema


class LikeableType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ACTIVITY', 'ACTIVITY_REPLY', 'THREAD', 'THREAD_COMMENT')


class MediaFormat(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('MANGA', 'MOVIE', 'MUSIC', 'NOVEL', 'ONA', 'ONE_SHOT', 'OVA', 'SPECIAL', 'TV', 'TV_SHORT')


class MediaListSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ADDED_TIME', 'ADDED_TIME_DESC', 'FINISHED_ON', 'FINISHED_ON_DESC', 'MEDIA_ID', 'MEDIA_ID_DESC', 'MEDIA_POPULARITY', 'MEDIA_POPULARITY_DESC', 'MEDIA_TITLE_ENGLISH', 'MEDIA_TITLE_ENGLISH_DESC', 'MEDIA_TITLE_NATIVE', 'MEDIA_TITLE_NATIVE_DESC', 'MEDIA_TITLE_ROMAJI', 'MEDIA_TITLE_ROMAJI_DESC', 'PRIORITY', 'PRIORITY_DESC', 'PROGRESS', 'PROGRESS_DESC', 'PROGRESS_VOLUMES', 'PROGRESS_VOLUMES_DESC', 'REPEAT', 'REPEAT_DESC', 'SCORE', 'SCORE_DESC', 'STARTED_ON', 'STARTED_ON_DESC', 'STATUS', 'STATUS_DESC', 'UPDATED_TIME', 'UPDATED_TIME_DESC')


class MediaListStatus(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('COMPLETED', 'CURRENT', 'DROPPED', 'PAUSED', 'PLANNING', 'REPEATING')


class MediaRankType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('POPULAR', 'RATED')


class MediaRelation(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ADAPTATION', 'ALTERNATIVE', 'CHARACTER', 'COMPILATION', 'CONTAINS', 'OTHER', 'PARENT', 'PREQUEL', 'SEQUEL', 'SIDE_STORY', 'SOURCE', 'SPIN_OFF', 'SUMMARY')


class MediaSeason(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('FALL', 'SPRING', 'SUMMER', 'WINTER')


class MediaSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CHAPTERS', 'CHAPTERS_DESC', 'DURATION', 'DURATION_DESC', 'END_DATE', 'END_DATE_DESC', 'EPISODES', 'EPISODES_DESC', 'FAVOURITES', 'FAVOURITES_DESC', 'FORMAT', 'FORMAT_DESC', 'ID', 'ID_DESC', 'POPULARITY', 'POPULARITY_DESC', 'SCORE', 'SCORE_DESC', 'SEARCH_MATCH', 'START_DATE', 'START_DATE_DESC', 'STATUS', 'STATUS_DESC', 'TITLE_ENGLISH', 'TITLE_ENGLISH_DESC', 'TITLE_NATIVE', 'TITLE_NATIVE_DESC', 'TITLE_ROMAJI', 'TITLE_ROMAJI_DESC', 'TRENDING', 'TRENDING_DESC', 'TYPE', 'TYPE_DESC', 'UPDATED_AT', 'UPDATED_AT_DESC', 'VOLUMES', 'VOLUMES_DESC')


class MediaSource(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ANIME', 'COMIC', 'DOUJINSHI', 'GAME', 'LIGHT_NOVEL', 'LIVE_ACTION', 'MANGA', 'MULTIMEDIA_PROJECT', 'NOVEL', 'ORIGINAL', 'OTHER', 'PICTURE_BOOK', 'VIDEO_GAME', 'VISUAL_NOVEL', 'WEB_NOVEL')


class MediaStatus(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CANCELLED', 'FINISHED', 'HIATUS', 'NOT_YET_RELEASED', 'RELEASING')


class MediaTrendSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('DATE', 'DATE_DESC', 'EPISODE', 'EPISODE_DESC', 'ID', 'ID_DESC', 'MEDIA_ID', 'MEDIA_ID_DESC', 'POPULARITY', 'POPULARITY_DESC', 'SCORE', 'SCORE_DESC', 'TRENDING', 'TRENDING_DESC')


class MediaType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ANIME', 'MANGA')


class ModActionType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ANON', 'BAN', 'DELETE', 'EDIT', 'EXPIRE', 'NOTE', 'REPORT', 'RESET')


class ModRole(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ADMIN', 'ANIME_DATA', 'COMMUNITY', 'DEVELOPER', 'DISCORD_COMMUNITY', 'LEAD_ANIME_DATA', 'LEAD_COMMUNITY', 'LEAD_DEVELOPER', 'LEAD_MANGA_DATA', 'LEAD_SOCIAL_MEDIA', 'MANGA_DATA', 'RETIRED', 'SOCIAL_MEDIA')


class NotificationType(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ACTIVITY_LIKE', 'ACTIVITY_MENTION', 'ACTIVITY_MESSAGE', 'ACTIVITY_REPLY', 'ACTIVITY_REPLY_LIKE', 'ACTIVITY_REPLY_SUBSCRIBED', 'AIRING', 'FOLLOWING', 'MEDIA_DATA_CHANGE', 'MEDIA_DELETION', 'MEDIA_MERGE', 'RELATED_MEDIA_ADDITION', 'THREAD_COMMENT_LIKE', 'THREAD_COMMENT_MENTION', 'THREAD_COMMENT_REPLY', 'THREAD_LIKE', 'THREAD_SUBSCRIBED')


class RecommendationRating(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('NO_RATING', 'RATE_DOWN', 'RATE_UP')


class RecommendationSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ID', 'ID_DESC', 'RATING', 'RATING_DESC')


class ReviewRating(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('DOWN_VOTE', 'NO_VOTE', 'UP_VOTE')


class ReviewSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CREATED_AT', 'CREATED_AT_DESC', 'ID', 'ID_DESC', 'RATING', 'RATING_DESC', 'SCORE', 'SCORE_DESC', 'UPDATED_AT', 'UPDATED_AT_DESC')


class RevisionHistoryAction(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CREATE', 'EDIT')


class ScoreFormat(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('POINT_10', 'POINT_100', 'POINT_10_DECIMAL', 'POINT_3', 'POINT_5')


class SiteTrendSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CHANGE', 'CHANGE_DESC', 'COUNT', 'COUNT_DESC', 'DATE', 'DATE_DESC')


class StaffLanguage(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ENGLISH', 'FRENCH', 'GERMAN', 'HEBREW', 'HUNGARIAN', 'ITALIAN', 'JAPANESE', 'KOREAN', 'PORTUGUESE', 'SPANISH')


class StaffSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('FAVOURITES', 'FAVOURITES_DESC', 'ID', 'ID_DESC', 'LANGUAGE', 'LANGUAGE_DESC', 'RELEVANCE', 'ROLE', 'ROLE_DESC', 'SEARCH_MATCH')


String = sgqlc.types.String

class StudioSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('FAVOURITES', 'FAVOURITES_DESC', 'ID', 'ID_DESC', 'NAME', 'NAME_DESC', 'SEARCH_MATCH')


class SubmissionSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ID', 'ID_DESC')


class SubmissionStatus(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ACCEPTED', 'PARTIALLY_ACCEPTED', 'PENDING', 'REJECTED')


class ThreadCommentSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ID', 'ID_DESC')


class ThreadSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CREATED_AT', 'CREATED_AT_DESC', 'ID', 'ID_DESC', 'IS_STICKY', 'REPLIED_AT', 'REPLIED_AT_DESC', 'REPLY_COUNT', 'REPLY_COUNT_DESC', 'SEARCH_MATCH', 'TITLE', 'TITLE_DESC', 'UPDATED_AT', 'UPDATED_AT_DESC', 'VIEW_COUNT', 'VIEW_COUNT_DESC')


class UserSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('CHAPTERS_READ', 'CHAPTERS_READ_DESC', 'ID', 'ID_DESC', 'SEARCH_MATCH', 'USERNAME', 'USERNAME_DESC', 'WATCHED_TIME', 'WATCHED_TIME_DESC')


class UserStaffNameLanguage(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('NATIVE', 'ROMAJI', 'ROMAJI_WESTERN')


class UserStatisticsSort(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('COUNT', 'COUNT_DESC', 'ID', 'ID_DESC', 'MEAN_SCORE', 'MEAN_SCORE_DESC', 'PROGRESS', 'PROGRESS_DESC')


class UserTitleLanguage(sgqlc.types.Enum):
    __schema__ = anilist_schema
    __choices__ = ('ENGLISH', 'ENGLISH_STYLISED', 'NATIVE', 'NATIVE_STYLISED', 'ROMAJI', 'ROMAJI_STYLISED')



########################################################################
# Input Objects
########################################################################
class AiringScheduleInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('airing_at', 'episode', 'time_until_airing')
    airing_at = sgqlc.types.Field(Int, graphql_name='airingAt')
    episode = sgqlc.types.Field(Int, graphql_name='episode')
    time_until_airing = sgqlc.types.Field(Int, graphql_name='timeUntilAiring')


class AniChartHighlightInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('media_id', 'highlight')
    media_id = sgqlc.types.Field(Int, graphql_name='mediaId')
    highlight = sgqlc.types.Field(String, graphql_name='highlight')


class CharacterNameInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('first', 'middle', 'last', 'native', 'alternative', 'alternative_spoiler')
    first = sgqlc.types.Field(String, graphql_name='first')
    middle = sgqlc.types.Field(String, graphql_name='middle')
    last = sgqlc.types.Field(String, graphql_name='last')
    native = sgqlc.types.Field(String, graphql_name='native')
    alternative = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alternative')
    alternative_spoiler = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alternativeSpoiler')


class FuzzyDateInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('year', 'month', 'day')
    year = sgqlc.types.Field(Int, graphql_name='year')
    month = sgqlc.types.Field(Int, graphql_name='month')
    day = sgqlc.types.Field(Int, graphql_name='day')


class ListActivityOptionInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('disabled', 'type')
    disabled = sgqlc.types.Field(Boolean, graphql_name='disabled')
    type = sgqlc.types.Field(MediaListStatus, graphql_name='type')


class MediaExternalLinkInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'url', 'site')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    site = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='site')


class MediaListOptionsInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('section_order', 'split_completed_section_by_format', 'custom_lists', 'advanced_scoring', 'advanced_scoring_enabled', 'theme')
    section_order = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='sectionOrder')
    split_completed_section_by_format = sgqlc.types.Field(Boolean, graphql_name='splitCompletedSectionByFormat')
    custom_lists = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='customLists')
    advanced_scoring = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='advancedScoring')
    advanced_scoring_enabled = sgqlc.types.Field(Boolean, graphql_name='advancedScoringEnabled')
    theme = sgqlc.types.Field(String, graphql_name='theme')


class MediaTitleInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('romaji', 'english', 'native')
    romaji = sgqlc.types.Field(String, graphql_name='romaji')
    english = sgqlc.types.Field(String, graphql_name='english')
    native = sgqlc.types.Field(String, graphql_name='native')


class NotificationOptionInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('type', 'enabled')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')


class StaffNameInput(sgqlc.types.Input):
    __schema__ = anilist_schema
    __field_names__ = ('first', 'middle', 'last', 'native', 'alternative')
    first = sgqlc.types.Field(String, graphql_name='first')
    middle = sgqlc.types.Field(String, graphql_name='middle')
    last = sgqlc.types.Field(String, graphql_name='last')
    native = sgqlc.types.Field(String, graphql_name='native')
    alternative = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alternative')



########################################################################
# Output Objects and Interfaces
########################################################################
class ActivityLikeNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'activity_id', 'context', 'created_at', 'activity', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    activity_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='activityId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    activity = sgqlc.types.Field('ActivityUnion', graphql_name='activity')
    user = sgqlc.types.Field('User', graphql_name='user')


class ActivityMentionNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'activity_id', 'context', 'created_at', 'activity', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    activity_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='activityId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    activity = sgqlc.types.Field('ActivityUnion', graphql_name='activity')
    user = sgqlc.types.Field('User', graphql_name='user')


class ActivityMessageNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'activity_id', 'context', 'created_at', 'message', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    activity_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='activityId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    message = sgqlc.types.Field('MessageActivity', graphql_name='message')
    user = sgqlc.types.Field('User', graphql_name='user')


class ActivityReply(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'activity_id', 'text', 'like_count', 'is_liked', 'created_at', 'user', 'likes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(Int, graphql_name='userId')
    activity_id = sgqlc.types.Field(Int, graphql_name='activityId')
    text = sgqlc.types.Field(String, graphql_name='text', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    like_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likeCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    user = sgqlc.types.Field('User', graphql_name='user')
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes')


class ActivityReplyLikeNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'activity_id', 'context', 'created_at', 'activity', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    activity_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='activityId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    activity = sgqlc.types.Field('ActivityUnion', graphql_name='activity')
    user = sgqlc.types.Field('User', graphql_name='user')


class ActivityReplyNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'activity_id', 'context', 'created_at', 'activity', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    activity_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='activityId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    activity = sgqlc.types.Field('ActivityUnion', graphql_name='activity')
    user = sgqlc.types.Field('User', graphql_name='user')


class ActivityReplySubscribedNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'activity_id', 'context', 'created_at', 'activity', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    activity_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='activityId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    activity = sgqlc.types.Field('ActivityUnion', graphql_name='activity')
    user = sgqlc.types.Field('User', graphql_name='user')


class AiringNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'type', 'anime_id', 'episode', 'contexts', 'created_at', 'media')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    anime_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='animeId')
    episode = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='episode')
    contexts = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='contexts')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    media = sgqlc.types.Field('Media', graphql_name='media')


class AiringProgression(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('episode', 'score', 'watching')
    episode = sgqlc.types.Field(Float, graphql_name='episode')
    score = sgqlc.types.Field(Float, graphql_name='score')
    watching = sgqlc.types.Field(Int, graphql_name='watching')


class AiringSchedule(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'airing_at', 'time_until_airing', 'episode', 'media_id', 'media')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    airing_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='airingAt')
    time_until_airing = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='timeUntilAiring')
    episode = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='episode')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    media = sgqlc.types.Field('Media', graphql_name='media')


class AiringScheduleConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('AiringScheduleEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(AiringSchedule), graphql_name='nodes')
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')


class AiringScheduleEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node', 'id')
    node = sgqlc.types.Field(AiringSchedule, graphql_name='node')
    id = sgqlc.types.Field(Int, graphql_name='id')


class AniChartUser(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('user', 'settings', 'highlights')
    user = sgqlc.types.Field('User', graphql_name='user')
    settings = sgqlc.types.Field(Json, graphql_name='settings')
    highlights = sgqlc.types.Field(Json, graphql_name='highlights')


class Character(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'name', 'image', 'description', 'gender', 'date_of_birth', 'age', 'blood_type', 'is_favourite', 'is_favourite_blocked', 'site_url', 'media', 'updated_at', 'favourites', 'mod_notes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    name = sgqlc.types.Field('CharacterName', graphql_name='name')
    image = sgqlc.types.Field('CharacterImage', graphql_name='image')
    description = sgqlc.types.Field(String, graphql_name='description', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    gender = sgqlc.types.Field(String, graphql_name='gender')
    date_of_birth = sgqlc.types.Field('FuzzyDate', graphql_name='dateOfBirth')
    age = sgqlc.types.Field(String, graphql_name='age')
    blood_type = sgqlc.types.Field(String, graphql_name='bloodType')
    is_favourite = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavourite')
    is_favourite_blocked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavouriteBlocked')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    media = sgqlc.types.Field('MediaConnection', graphql_name='media', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    updated_at = sgqlc.types.Field(Int, graphql_name='updatedAt')
    favourites = sgqlc.types.Field(Int, graphql_name='favourites')
    mod_notes = sgqlc.types.Field(String, graphql_name='modNotes')


class CharacterConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CharacterEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Character), graphql_name='nodes')
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')


class CharacterEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node', 'id', 'role', 'name', 'voice_actors', 'voice_actor_roles', 'media', 'favourite_order')
    node = sgqlc.types.Field(Character, graphql_name='node')
    id = sgqlc.types.Field(Int, graphql_name='id')
    role = sgqlc.types.Field(CharacterRole, graphql_name='role')
    name = sgqlc.types.Field(String, graphql_name='name')
    voice_actors = sgqlc.types.Field(sgqlc.types.list_of('Staff'), graphql_name='voiceActors', args=sgqlc.types.ArgDict((
        ('language', sgqlc.types.Arg(StaffLanguage, graphql_name='language', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    voice_actor_roles = sgqlc.types.Field(sgqlc.types.list_of('StaffRoleType'), graphql_name='voiceActorRoles', args=sgqlc.types.ArgDict((
        ('language', sgqlc.types.Arg(StaffLanguage, graphql_name='language', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    media = sgqlc.types.Field(sgqlc.types.list_of('Media'), graphql_name='media')
    favourite_order = sgqlc.types.Field(Int, graphql_name='favouriteOrder')


class CharacterImage(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('large', 'medium')
    large = sgqlc.types.Field(String, graphql_name='large')
    medium = sgqlc.types.Field(String, graphql_name='medium')


class CharacterName(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('first', 'middle', 'last', 'full', 'native', 'alternative', 'alternative_spoiler', 'user_preferred')
    first = sgqlc.types.Field(String, graphql_name='first')
    middle = sgqlc.types.Field(String, graphql_name='middle')
    last = sgqlc.types.Field(String, graphql_name='last')
    full = sgqlc.types.Field(String, graphql_name='full')
    native = sgqlc.types.Field(String, graphql_name='native')
    alternative = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alternative')
    alternative_spoiler = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alternativeSpoiler')
    user_preferred = sgqlc.types.Field(String, graphql_name='userPreferred')


class CharacterSubmission(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'character', 'submission', 'submitter', 'assignee', 'status', 'notes', 'source', 'locked', 'created_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    character = sgqlc.types.Field(Character, graphql_name='character')
    submission = sgqlc.types.Field(Character, graphql_name='submission')
    submitter = sgqlc.types.Field('User', graphql_name='submitter')
    assignee = sgqlc.types.Field('User', graphql_name='assignee')
    status = sgqlc.types.Field(SubmissionStatus, graphql_name='status')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    source = sgqlc.types.Field(String, graphql_name='source')
    locked = sgqlc.types.Field(Boolean, graphql_name='locked')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')


class CharacterSubmissionConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('CharacterSubmissionEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(CharacterSubmission), graphql_name='nodes')
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')


class CharacterSubmissionEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node', 'role', 'voice_actors', 'submitted_voice_actors')
    node = sgqlc.types.Field(CharacterSubmission, graphql_name='node')
    role = sgqlc.types.Field(CharacterRole, graphql_name='role')
    voice_actors = sgqlc.types.Field(sgqlc.types.list_of('Staff'), graphql_name='voiceActors')
    submitted_voice_actors = sgqlc.types.Field(sgqlc.types.list_of('StaffSubmission'), graphql_name='submittedVoiceActors')


class Deleted(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('deleted',)
    deleted = sgqlc.types.Field(Boolean, graphql_name='deleted')


class Favourites(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('anime', 'manga', 'characters', 'staff', 'studios')
    anime = sgqlc.types.Field('MediaConnection', graphql_name='anime', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    manga = sgqlc.types.Field('MediaConnection', graphql_name='manga', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    characters = sgqlc.types.Field(CharacterConnection, graphql_name='characters', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    staff = sgqlc.types.Field('StaffConnection', graphql_name='staff', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    studios = sgqlc.types.Field('StudioConnection', graphql_name='studios', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )


class FollowingNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'context', 'created_at', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    user = sgqlc.types.Field('User', graphql_name='user')


class FormatStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('format', 'amount')
    format = sgqlc.types.Field(MediaFormat, graphql_name='format')
    amount = sgqlc.types.Field(Int, graphql_name='amount')


class FuzzyDate(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('year', 'month', 'day')
    year = sgqlc.types.Field(Int, graphql_name='year')
    month = sgqlc.types.Field(Int, graphql_name='month')
    day = sgqlc.types.Field(Int, graphql_name='day')


class GenreStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('genre', 'amount', 'mean_score', 'time_watched')
    genre = sgqlc.types.Field(String, graphql_name='genre')
    amount = sgqlc.types.Field(Int, graphql_name='amount')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')
    time_watched = sgqlc.types.Field(Int, graphql_name='timeWatched')


class InternalPage(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('media_submissions', 'character_submissions', 'staff_submissions', 'revision_history', 'reports', 'mod_actions', 'user_block_search', 'page_info', 'users', 'media', 'characters', 'staff', 'studios', 'media_list', 'airing_schedules', 'media_trends', 'notifications', 'followers', 'following', 'activities', 'activity_replies', 'threads', 'thread_comments', 'reviews', 'recommendations', 'likes')
    media_submissions = sgqlc.types.Field(sgqlc.types.list_of('MediaSubmission'), graphql_name='mediaSubmissions', args=sgqlc.types.ArgDict((
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('submission_id', sgqlc.types.Arg(Int, graphql_name='submissionId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('assignee_id', sgqlc.types.Arg(Int, graphql_name='assigneeId', default=None)),
        ('status', sgqlc.types.Arg(SubmissionStatus, graphql_name='status', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SubmissionSort), graphql_name='sort', default=None)),
))
    )
    character_submissions = sgqlc.types.Field(sgqlc.types.list_of(CharacterSubmission), graphql_name='characterSubmissions', args=sgqlc.types.ArgDict((
        ('character_id', sgqlc.types.Arg(Int, graphql_name='characterId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('assignee_id', sgqlc.types.Arg(Int, graphql_name='assigneeId', default=None)),
        ('status', sgqlc.types.Arg(SubmissionStatus, graphql_name='status', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SubmissionSort), graphql_name='sort', default=None)),
))
    )
    staff_submissions = sgqlc.types.Field(sgqlc.types.list_of('StaffSubmission'), graphql_name='staffSubmissions', args=sgqlc.types.ArgDict((
        ('staff_id', sgqlc.types.Arg(Int, graphql_name='staffId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('assignee_id', sgqlc.types.Arg(Int, graphql_name='assigneeId', default=None)),
        ('status', sgqlc.types.Arg(SubmissionStatus, graphql_name='status', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SubmissionSort), graphql_name='sort', default=None)),
))
    )
    revision_history = sgqlc.types.Field(sgqlc.types.list_of('RevisionHistory'), graphql_name='revisionHistory', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('character_id', sgqlc.types.Arg(Int, graphql_name='characterId', default=None)),
        ('staff_id', sgqlc.types.Arg(Int, graphql_name='staffId', default=None)),
        ('studio_id', sgqlc.types.Arg(Int, graphql_name='studioId', default=None)),
))
    )
    reports = sgqlc.types.Field(sgqlc.types.list_of('Report'), graphql_name='reports', args=sgqlc.types.ArgDict((
        ('reporter_id', sgqlc.types.Arg(Int, graphql_name='reporterId', default=None)),
        ('reported_id', sgqlc.types.Arg(Int, graphql_name='reportedId', default=None)),
))
    )
    mod_actions = sgqlc.types.Field(sgqlc.types.list_of('ModAction'), graphql_name='modActions', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('mod_id', sgqlc.types.Arg(Int, graphql_name='modId', default=None)),
))
    )
    user_block_search = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='userBlockSearch', args=sgqlc.types.ArgDict((
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
))
    )
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')
    users = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='users', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('is_moderator', sgqlc.types.Arg(Boolean, graphql_name='isModerator', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    media = sgqlc.types.Field(sgqlc.types.list_of('Media'), graphql_name='media', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('id_mal', sgqlc.types.Arg(Int, graphql_name='idMal', default=None)),
        ('start_date', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate', default=None)),
        ('end_date', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate', default=None)),
        ('season', sgqlc.types.Arg(MediaSeason, graphql_name='season', default=None)),
        ('season_year', sgqlc.types.Arg(Int, graphql_name='seasonYear', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('format', sgqlc.types.Arg(MediaFormat, graphql_name='format', default=None)),
        ('status', sgqlc.types.Arg(MediaStatus, graphql_name='status', default=None)),
        ('episodes', sgqlc.types.Arg(Int, graphql_name='episodes', default=None)),
        ('duration', sgqlc.types.Arg(Int, graphql_name='duration', default=None)),
        ('chapters', sgqlc.types.Arg(Int, graphql_name='chapters', default=None)),
        ('volumes', sgqlc.types.Arg(Int, graphql_name='volumes', default=None)),
        ('is_adult', sgqlc.types.Arg(Boolean, graphql_name='isAdult', default=None)),
        ('genre', sgqlc.types.Arg(String, graphql_name='genre', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('minimum_tag_rank', sgqlc.types.Arg(Int, graphql_name='minimumTagRank', default=None)),
        ('tag_category', sgqlc.types.Arg(String, graphql_name='tagCategory', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('licensed_by', sgqlc.types.Arg(String, graphql_name='licensedBy', default=None)),
        ('licensed_by_id', sgqlc.types.Arg(Int, graphql_name='licensedById', default=None)),
        ('average_score', sgqlc.types.Arg(Int, graphql_name='averageScore', default=None)),
        ('popularity', sgqlc.types.Arg(Int, graphql_name='popularity', default=None)),
        ('source', sgqlc.types.Arg(MediaSource, graphql_name='source', default=None)),
        ('country_of_origin', sgqlc.types.Arg(CountryCode, graphql_name='countryOfOrigin', default=None)),
        ('is_licensed', sgqlc.types.Arg(Boolean, graphql_name='isLicensed', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('id_mal_not', sgqlc.types.Arg(Int, graphql_name='idMal_not', default=None)),
        ('id_mal_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='idMal_in', default=None)),
        ('id_mal_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='idMal_not_in', default=None)),
        ('start_date_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate_greater', default=None)),
        ('start_date_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate_lesser', default=None)),
        ('start_date_like', sgqlc.types.Arg(String, graphql_name='startDate_like', default=None)),
        ('end_date_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate_greater', default=None)),
        ('end_date_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate_lesser', default=None)),
        ('end_date_like', sgqlc.types.Arg(String, graphql_name='endDate_like', default=None)),
        ('format_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaFormat), graphql_name='format_in', default=None)),
        ('format_not', sgqlc.types.Arg(MediaFormat, graphql_name='format_not', default=None)),
        ('format_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaFormat), graphql_name='format_not_in', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaStatus), graphql_name='status_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaStatus, graphql_name='status_not', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaStatus), graphql_name='status_not_in', default=None)),
        ('episodes_greater', sgqlc.types.Arg(Int, graphql_name='episodes_greater', default=None)),
        ('episodes_lesser', sgqlc.types.Arg(Int, graphql_name='episodes_lesser', default=None)),
        ('duration_greater', sgqlc.types.Arg(Int, graphql_name='duration_greater', default=None)),
        ('duration_lesser', sgqlc.types.Arg(Int, graphql_name='duration_lesser', default=None)),
        ('chapters_greater', sgqlc.types.Arg(Int, graphql_name='chapters_greater', default=None)),
        ('chapters_lesser', sgqlc.types.Arg(Int, graphql_name='chapters_lesser', default=None)),
        ('volumes_greater', sgqlc.types.Arg(Int, graphql_name='volumes_greater', default=None)),
        ('volumes_lesser', sgqlc.types.Arg(Int, graphql_name='volumes_lesser', default=None)),
        ('genre_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='genre_in', default=None)),
        ('genre_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='genre_not_in', default=None)),
        ('tag_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tag_in', default=None)),
        ('tag_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tag_not_in', default=None)),
        ('tag_category_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tagCategory_in', default=None)),
        ('tag_category_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tagCategory_not_in', default=None)),
        ('licensed_by_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='licensedBy_in', default=None)),
        ('licensed_by_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='licensedById_in', default=None)),
        ('average_score_not', sgqlc.types.Arg(Int, graphql_name='averageScore_not', default=None)),
        ('average_score_greater', sgqlc.types.Arg(Int, graphql_name='averageScore_greater', default=None)),
        ('average_score_lesser', sgqlc.types.Arg(Int, graphql_name='averageScore_lesser', default=None)),
        ('popularity_not', sgqlc.types.Arg(Int, graphql_name='popularity_not', default=None)),
        ('popularity_greater', sgqlc.types.Arg(Int, graphql_name='popularity_greater', default=None)),
        ('popularity_lesser', sgqlc.types.Arg(Int, graphql_name='popularity_lesser', default=None)),
        ('source_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaSource), graphql_name='source_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
))
    )
    characters = sgqlc.types.Field(sgqlc.types.list_of(Character), graphql_name='characters', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('is_birthday', sgqlc.types.Arg(Boolean, graphql_name='isBirthday', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(CharacterSort), graphql_name='sort', default=None)),
))
    )
    staff = sgqlc.types.Field(sgqlc.types.list_of('Staff'), graphql_name='staff', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('is_birthday', sgqlc.types.Arg(Boolean, graphql_name='isBirthday', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    studios = sgqlc.types.Field(sgqlc.types.list_of('Studio'), graphql_name='studios', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StudioSort), graphql_name='sort', default=None)),
))
    )
    media_list = sgqlc.types.Field(sgqlc.types.list_of('MediaList'), graphql_name='mediaList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('user_name', sgqlc.types.Arg(String, graphql_name='userName', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('status', sgqlc.types.Arg(MediaListStatus, graphql_name='status', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('is_following', sgqlc.types.Arg(Boolean, graphql_name='isFollowing', default=None)),
        ('notes', sgqlc.types.Arg(String, graphql_name='notes', default=None)),
        ('started_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt', default=None)),
        ('completed_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt', default=None)),
        ('compare_with_auth_list', sgqlc.types.Arg(Boolean, graphql_name='compareWithAuthList', default=None)),
        ('user_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_in', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_in', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_not_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaListStatus, graphql_name='status_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('notes_like', sgqlc.types.Arg(String, graphql_name='notes_like', default=None)),
        ('started_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_greater', default=None)),
        ('started_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_lesser', default=None)),
        ('started_at_like', sgqlc.types.Arg(String, graphql_name='startedAt_like', default=None)),
        ('completed_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_greater', default=None)),
        ('completed_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_lesser', default=None)),
        ('completed_at_like', sgqlc.types.Arg(String, graphql_name='completedAt_like', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaListSort), graphql_name='sort', default=None)),
))
    )
    airing_schedules = sgqlc.types.Field(sgqlc.types.list_of(AiringSchedule), graphql_name='airingSchedules', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('episode', sgqlc.types.Arg(Int, graphql_name='episode', default=None)),
        ('airing_at', sgqlc.types.Arg(Int, graphql_name='airingAt', default=None)),
        ('not_yet_aired', sgqlc.types.Arg(Boolean, graphql_name='notYetAired', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('episode_not', sgqlc.types.Arg(Int, graphql_name='episode_not', default=None)),
        ('episode_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='episode_in', default=None)),
        ('episode_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='episode_not_in', default=None)),
        ('episode_greater', sgqlc.types.Arg(Int, graphql_name='episode_greater', default=None)),
        ('episode_lesser', sgqlc.types.Arg(Int, graphql_name='episode_lesser', default=None)),
        ('airing_at_greater', sgqlc.types.Arg(Int, graphql_name='airingAt_greater', default=None)),
        ('airing_at_lesser', sgqlc.types.Arg(Int, graphql_name='airingAt_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(AiringSort), graphql_name='sort', default=None)),
))
    )
    media_trends = sgqlc.types.Field(sgqlc.types.list_of('MediaTrend'), graphql_name='mediaTrends', args=sgqlc.types.ArgDict((
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('date', sgqlc.types.Arg(Int, graphql_name='date', default=None)),
        ('trending', sgqlc.types.Arg(Int, graphql_name='trending', default=None)),
        ('average_score', sgqlc.types.Arg(Int, graphql_name='averageScore', default=None)),
        ('popularity', sgqlc.types.Arg(Int, graphql_name='popularity', default=None)),
        ('episode', sgqlc.types.Arg(Int, graphql_name='episode', default=None)),
        ('releasing', sgqlc.types.Arg(Boolean, graphql_name='releasing', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('date_greater', sgqlc.types.Arg(Int, graphql_name='date_greater', default=None)),
        ('date_lesser', sgqlc.types.Arg(Int, graphql_name='date_lesser', default=None)),
        ('trending_greater', sgqlc.types.Arg(Int, graphql_name='trending_greater', default=None)),
        ('trending_lesser', sgqlc.types.Arg(Int, graphql_name='trending_lesser', default=None)),
        ('trending_not', sgqlc.types.Arg(Int, graphql_name='trending_not', default=None)),
        ('average_score_greater', sgqlc.types.Arg(Int, graphql_name='averageScore_greater', default=None)),
        ('average_score_lesser', sgqlc.types.Arg(Int, graphql_name='averageScore_lesser', default=None)),
        ('average_score_not', sgqlc.types.Arg(Int, graphql_name='averageScore_not', default=None)),
        ('popularity_greater', sgqlc.types.Arg(Int, graphql_name='popularity_greater', default=None)),
        ('popularity_lesser', sgqlc.types.Arg(Int, graphql_name='popularity_lesser', default=None)),
        ('popularity_not', sgqlc.types.Arg(Int, graphql_name='popularity_not', default=None)),
        ('episode_greater', sgqlc.types.Arg(Int, graphql_name='episode_greater', default=None)),
        ('episode_lesser', sgqlc.types.Arg(Int, graphql_name='episode_lesser', default=None)),
        ('episode_not', sgqlc.types.Arg(Int, graphql_name='episode_not', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaTrendSort), graphql_name='sort', default=None)),
))
    )
    notifications = sgqlc.types.Field(sgqlc.types.list_of('NotificationUnion'), graphql_name='notifications', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(NotificationType, graphql_name='type', default=None)),
        ('reset_notification_count', sgqlc.types.Arg(Boolean, graphql_name='resetNotificationCount', default=None)),
        ('type_in', sgqlc.types.Arg(sgqlc.types.list_of(NotificationType), graphql_name='type_in', default=None)),
))
    )
    followers = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='followers', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    following = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='following', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    activities = sgqlc.types.Field(sgqlc.types.list_of('ActivityUnion'), graphql_name='activities', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('messenger_id', sgqlc.types.Arg(Int, graphql_name='messengerId', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('type', sgqlc.types.Arg(ActivityType, graphql_name='type', default=None)),
        ('is_following', sgqlc.types.Arg(Boolean, graphql_name='isFollowing', default=None)),
        ('has_replies', sgqlc.types.Arg(Boolean, graphql_name='hasReplies', default=None)),
        ('has_replies_or_type_text', sgqlc.types.Arg(Boolean, graphql_name='hasRepliesOrTypeText', default=None)),
        ('created_at', sgqlc.types.Arg(Int, graphql_name='createdAt', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('user_id_not', sgqlc.types.Arg(Int, graphql_name='userId_not', default=None)),
        ('user_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_in', default=None)),
        ('user_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_not_in', default=None)),
        ('messenger_id_not', sgqlc.types.Arg(Int, graphql_name='messengerId_not', default=None)),
        ('messenger_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='messengerId_in', default=None)),
        ('messenger_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='messengerId_not_in', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('type_not', sgqlc.types.Arg(ActivityType, graphql_name='type_not', default=None)),
        ('type_in', sgqlc.types.Arg(sgqlc.types.list_of(ActivityType), graphql_name='type_in', default=None)),
        ('type_not_in', sgqlc.types.Arg(sgqlc.types.list_of(ActivityType), graphql_name='type_not_in', default=None)),
        ('created_at_greater', sgqlc.types.Arg(Int, graphql_name='createdAt_greater', default=None)),
        ('created_at_lesser', sgqlc.types.Arg(Int, graphql_name='createdAt_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ActivitySort), graphql_name='sort', default=None)),
))
    )
    activity_replies = sgqlc.types.Field(sgqlc.types.list_of(ActivityReply), graphql_name='activityReplies', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('activity_id', sgqlc.types.Arg(Int, graphql_name='activityId', default=None)),
))
    )
    threads = sgqlc.types.Field(sgqlc.types.list_of('Thread'), graphql_name='threads', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('reply_user_id', sgqlc.types.Arg(Int, graphql_name='replyUserId', default=None)),
        ('subscribed', sgqlc.types.Arg(Boolean, graphql_name='subscribed', default=None)),
        ('category_id', sgqlc.types.Arg(Int, graphql_name='categoryId', default=None)),
        ('media_category_id', sgqlc.types.Arg(Int, graphql_name='mediaCategoryId', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ThreadSort), graphql_name='sort', default=None)),
))
    )
    thread_comments = sgqlc.types.Field(sgqlc.types.list_of('ThreadComment'), graphql_name='threadComments', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('thread_id', sgqlc.types.Arg(Int, graphql_name='threadId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ThreadCommentSort), graphql_name='sort', default=None)),
))
    )
    reviews = sgqlc.types.Field(sgqlc.types.list_of('Review'), graphql_name='reviews', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('media_type', sgqlc.types.Arg(MediaType, graphql_name='mediaType', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ReviewSort), graphql_name='sort', default=None)),
))
    )
    recommendations = sgqlc.types.Field(sgqlc.types.list_of('Recommendation'), graphql_name='recommendations', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('media_recommendation_id', sgqlc.types.Arg(Int, graphql_name='mediaRecommendationId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('rating', sgqlc.types.Arg(Int, graphql_name='rating', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('rating_greater', sgqlc.types.Arg(Int, graphql_name='rating_greater', default=None)),
        ('rating_lesser', sgqlc.types.Arg(Int, graphql_name='rating_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(RecommendationSort), graphql_name='sort', default=None)),
))
    )
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes', args=sgqlc.types.ArgDict((
        ('likeable_id', sgqlc.types.Arg(Int, graphql_name='likeableId', default=None)),
        ('type', sgqlc.types.Arg(LikeableType, graphql_name='type', default=None)),
))
    )


class ListActivity(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'reply_count', 'status', 'progress', 'is_locked', 'is_subscribed', 'like_count', 'is_liked', 'is_pinned', 'site_url', 'created_at', 'user', 'media', 'replies', 'likes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(Int, graphql_name='userId')
    type = sgqlc.types.Field(ActivityType, graphql_name='type')
    reply_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='replyCount')
    status = sgqlc.types.Field(String, graphql_name='status')
    progress = sgqlc.types.Field(String, graphql_name='progress')
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')
    is_subscribed = sgqlc.types.Field(Boolean, graphql_name='isSubscribed')
    like_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likeCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    is_pinned = sgqlc.types.Field(Boolean, graphql_name='isPinned')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    user = sgqlc.types.Field('User', graphql_name='user')
    media = sgqlc.types.Field('Media', graphql_name='media')
    replies = sgqlc.types.Field(sgqlc.types.list_of(ActivityReply), graphql_name='replies')
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes')


class ListActivityOption(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('disabled', 'type')
    disabled = sgqlc.types.Field(Boolean, graphql_name='disabled')
    type = sgqlc.types.Field(MediaListStatus, graphql_name='type')


class ListScoreStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('mean_score', 'standard_deviation')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')
    standard_deviation = sgqlc.types.Field(Int, graphql_name='standardDeviation')


class Media(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'id_mal', 'title', 'type', 'format', 'status', 'description', 'start_date', 'end_date', 'season', 'season_year', 'season_int', 'episodes', 'duration', 'chapters', 'volumes', 'country_of_origin', 'is_licensed', 'source', 'hashtag', 'trailer', 'updated_at', 'cover_image', 'banner_image', 'genres', 'synonyms', 'average_score', 'mean_score', 'popularity', 'is_locked', 'trending', 'favourites', 'tags', 'relations', 'characters', 'staff', 'studios', 'is_favourite', 'is_favourite_blocked', 'is_adult', 'next_airing_episode', 'airing_schedule', 'trends', 'external_links', 'streaming_episodes', 'rankings', 'media_list_entry', 'reviews', 'recommendations', 'stats', 'site_url', 'auto_create_forum_thread', 'is_recommendation_blocked', 'is_review_blocked', 'mod_notes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    id_mal = sgqlc.types.Field(Int, graphql_name='idMal')
    title = sgqlc.types.Field('MediaTitle', graphql_name='title')
    type = sgqlc.types.Field(MediaType, graphql_name='type')
    format = sgqlc.types.Field(MediaFormat, graphql_name='format')
    status = sgqlc.types.Field(MediaStatus, graphql_name='status', args=sgqlc.types.ArgDict((
        ('version', sgqlc.types.Arg(Int, graphql_name='version', default=None)),
))
    )
    description = sgqlc.types.Field(String, graphql_name='description', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    start_date = sgqlc.types.Field(FuzzyDate, graphql_name='startDate')
    end_date = sgqlc.types.Field(FuzzyDate, graphql_name='endDate')
    season = sgqlc.types.Field(MediaSeason, graphql_name='season')
    season_year = sgqlc.types.Field(Int, graphql_name='seasonYear')
    season_int = sgqlc.types.Field(Int, graphql_name='seasonInt')
    episodes = sgqlc.types.Field(Int, graphql_name='episodes')
    duration = sgqlc.types.Field(Int, graphql_name='duration')
    chapters = sgqlc.types.Field(Int, graphql_name='chapters')
    volumes = sgqlc.types.Field(Int, graphql_name='volumes')
    country_of_origin = sgqlc.types.Field(CountryCode, graphql_name='countryOfOrigin')
    is_licensed = sgqlc.types.Field(Boolean, graphql_name='isLicensed')
    source = sgqlc.types.Field(MediaSource, graphql_name='source', args=sgqlc.types.ArgDict((
        ('version', sgqlc.types.Arg(Int, graphql_name='version', default=None)),
))
    )
    hashtag = sgqlc.types.Field(String, graphql_name='hashtag')
    trailer = sgqlc.types.Field('MediaTrailer', graphql_name='trailer')
    updated_at = sgqlc.types.Field(Int, graphql_name='updatedAt')
    cover_image = sgqlc.types.Field('MediaCoverImage', graphql_name='coverImage')
    banner_image = sgqlc.types.Field(String, graphql_name='bannerImage')
    genres = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='genres')
    synonyms = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='synonyms')
    average_score = sgqlc.types.Field(Int, graphql_name='averageScore')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')
    popularity = sgqlc.types.Field(Int, graphql_name='popularity')
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')
    trending = sgqlc.types.Field(Int, graphql_name='trending')
    favourites = sgqlc.types.Field(Int, graphql_name='favourites')
    tags = sgqlc.types.Field(sgqlc.types.list_of('MediaTag'), graphql_name='tags')
    relations = sgqlc.types.Field('MediaConnection', graphql_name='relations')
    characters = sgqlc.types.Field(CharacterConnection, graphql_name='characters', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(CharacterSort), graphql_name='sort', default=None)),
        ('role', sgqlc.types.Arg(CharacterRole, graphql_name='role', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    staff = sgqlc.types.Field('StaffConnection', graphql_name='staff', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    studios = sgqlc.types.Field('StudioConnection', graphql_name='studios', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StudioSort), graphql_name='sort', default=None)),
        ('is_main', sgqlc.types.Arg(Boolean, graphql_name='isMain', default=None)),
))
    )
    is_favourite = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavourite')
    is_favourite_blocked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavouriteBlocked')
    is_adult = sgqlc.types.Field(Boolean, graphql_name='isAdult')
    next_airing_episode = sgqlc.types.Field(AiringSchedule, graphql_name='nextAiringEpisode')
    airing_schedule = sgqlc.types.Field(AiringScheduleConnection, graphql_name='airingSchedule', args=sgqlc.types.ArgDict((
        ('not_yet_aired', sgqlc.types.Arg(Boolean, graphql_name='notYetAired', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    trends = sgqlc.types.Field('MediaTrendConnection', graphql_name='trends', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaTrendSort), graphql_name='sort', default=None)),
        ('releasing', sgqlc.types.Arg(Boolean, graphql_name='releasing', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    external_links = sgqlc.types.Field(sgqlc.types.list_of('MediaExternalLink'), graphql_name='externalLinks')
    streaming_episodes = sgqlc.types.Field(sgqlc.types.list_of('MediaStreamingEpisode'), graphql_name='streamingEpisodes')
    rankings = sgqlc.types.Field(sgqlc.types.list_of('MediaRank'), graphql_name='rankings')
    media_list_entry = sgqlc.types.Field('MediaList', graphql_name='mediaListEntry')
    reviews = sgqlc.types.Field('ReviewConnection', graphql_name='reviews', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ReviewSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    recommendations = sgqlc.types.Field('RecommendationConnection', graphql_name='recommendations', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(RecommendationSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    stats = sgqlc.types.Field('MediaStats', graphql_name='stats')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    auto_create_forum_thread = sgqlc.types.Field(Boolean, graphql_name='autoCreateForumThread')
    is_recommendation_blocked = sgqlc.types.Field(Boolean, graphql_name='isRecommendationBlocked')
    is_review_blocked = sgqlc.types.Field(Boolean, graphql_name='isReviewBlocked')
    mod_notes = sgqlc.types.Field(String, graphql_name='modNotes')


class MediaCharacter(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'role', 'role_notes', 'dub_group', 'character_name', 'character', 'voice_actor')
    id = sgqlc.types.Field(Int, graphql_name='id')
    role = sgqlc.types.Field(CharacterRole, graphql_name='role')
    role_notes = sgqlc.types.Field(String, graphql_name='roleNotes')
    dub_group = sgqlc.types.Field(String, graphql_name='dubGroup')
    character_name = sgqlc.types.Field(String, graphql_name='characterName')
    character = sgqlc.types.Field(Character, graphql_name='character')
    voice_actor = sgqlc.types.Field('Staff', graphql_name='voiceActor')


class MediaConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MediaEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Media), graphql_name='nodes')
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')


class MediaCoverImage(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('extra_large', 'large', 'medium', 'color')
    extra_large = sgqlc.types.Field(String, graphql_name='extraLarge')
    large = sgqlc.types.Field(String, graphql_name='large')
    medium = sgqlc.types.Field(String, graphql_name='medium')
    color = sgqlc.types.Field(String, graphql_name='color')


class MediaDataChangeNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'type', 'media_id', 'context', 'reason', 'created_at', 'media')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    context = sgqlc.types.Field(String, graphql_name='context')
    reason = sgqlc.types.Field(String, graphql_name='reason')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    media = sgqlc.types.Field(Media, graphql_name='media')


class MediaDeletionNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'type', 'deleted_media_title', 'context', 'reason', 'created_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    deleted_media_title = sgqlc.types.Field(String, graphql_name='deletedMediaTitle')
    context = sgqlc.types.Field(String, graphql_name='context')
    reason = sgqlc.types.Field(String, graphql_name='reason')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')


class MediaEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node', 'id', 'relation_type', 'is_main_studio', 'characters', 'character_role', 'character_name', 'role_notes', 'dub_group', 'staff_role', 'voice_actors', 'voice_actor_roles', 'favourite_order')
    node = sgqlc.types.Field(Media, graphql_name='node')
    id = sgqlc.types.Field(Int, graphql_name='id')
    relation_type = sgqlc.types.Field(MediaRelation, graphql_name='relationType', args=sgqlc.types.ArgDict((
        ('version', sgqlc.types.Arg(Int, graphql_name='version', default=None)),
))
    )
    is_main_studio = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isMainStudio')
    characters = sgqlc.types.Field(sgqlc.types.list_of(Character), graphql_name='characters')
    character_role = sgqlc.types.Field(CharacterRole, graphql_name='characterRole')
    character_name = sgqlc.types.Field(String, graphql_name='characterName')
    role_notes = sgqlc.types.Field(String, graphql_name='roleNotes')
    dub_group = sgqlc.types.Field(String, graphql_name='dubGroup')
    staff_role = sgqlc.types.Field(String, graphql_name='staffRole')
    voice_actors = sgqlc.types.Field(sgqlc.types.list_of('Staff'), graphql_name='voiceActors', args=sgqlc.types.ArgDict((
        ('language', sgqlc.types.Arg(StaffLanguage, graphql_name='language', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    voice_actor_roles = sgqlc.types.Field(sgqlc.types.list_of('StaffRoleType'), graphql_name='voiceActorRoles', args=sgqlc.types.ArgDict((
        ('language', sgqlc.types.Arg(StaffLanguage, graphql_name='language', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    favourite_order = sgqlc.types.Field(Int, graphql_name='favouriteOrder')


class MediaExternalLink(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'url', 'site', 'site_id', 'type', 'language', 'color', 'icon', 'notes', 'is_disabled')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    url = sgqlc.types.Field(String, graphql_name='url')
    site = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='site')
    site_id = sgqlc.types.Field(Int, graphql_name='siteId')
    type = sgqlc.types.Field(ExternalLinkType, graphql_name='type')
    language = sgqlc.types.Field(String, graphql_name='language')
    color = sgqlc.types.Field(String, graphql_name='color')
    icon = sgqlc.types.Field(String, graphql_name='icon')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    is_disabled = sgqlc.types.Field(Boolean, graphql_name='isDisabled')


class MediaList(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'media_id', 'status', 'score', 'progress', 'progress_volumes', 'repeat', 'priority', 'private', 'notes', 'hidden_from_status_lists', 'custom_lists', 'advanced_scores', 'started_at', 'completed_at', 'updated_at', 'created_at', 'media', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    status = sgqlc.types.Field(MediaListStatus, graphql_name='status')
    score = sgqlc.types.Field(Float, graphql_name='score', args=sgqlc.types.ArgDict((
        ('format', sgqlc.types.Arg(ScoreFormat, graphql_name='format', default=None)),
))
    )
    progress = sgqlc.types.Field(Int, graphql_name='progress')
    progress_volumes = sgqlc.types.Field(Int, graphql_name='progressVolumes')
    repeat = sgqlc.types.Field(Int, graphql_name='repeat')
    priority = sgqlc.types.Field(Int, graphql_name='priority')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    hidden_from_status_lists = sgqlc.types.Field(Boolean, graphql_name='hiddenFromStatusLists')
    custom_lists = sgqlc.types.Field(Json, graphql_name='customLists', args=sgqlc.types.ArgDict((
        ('as_array', sgqlc.types.Arg(Boolean, graphql_name='asArray', default=None)),
))
    )
    advanced_scores = sgqlc.types.Field(Json, graphql_name='advancedScores')
    started_at = sgqlc.types.Field(FuzzyDate, graphql_name='startedAt')
    completed_at = sgqlc.types.Field(FuzzyDate, graphql_name='completedAt')
    updated_at = sgqlc.types.Field(Int, graphql_name='updatedAt')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    media = sgqlc.types.Field(Media, graphql_name='media')
    user = sgqlc.types.Field('User', graphql_name='user')


class MediaListCollection(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('lists', 'user', 'has_next_chunk', 'status_lists', 'custom_lists')
    lists = sgqlc.types.Field(sgqlc.types.list_of('MediaListGroup'), graphql_name='lists')
    user = sgqlc.types.Field('User', graphql_name='user')
    has_next_chunk = sgqlc.types.Field(Boolean, graphql_name='hasNextChunk')
    status_lists = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.list_of(MediaList)), graphql_name='statusLists', args=sgqlc.types.ArgDict((
        ('as_array', sgqlc.types.Arg(Boolean, graphql_name='asArray', default=None)),
))
    )
    custom_lists = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.list_of(MediaList)), graphql_name='customLists', args=sgqlc.types.ArgDict((
        ('as_array', sgqlc.types.Arg(Boolean, graphql_name='asArray', default=None)),
))
    )


class MediaListGroup(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('entries', 'name', 'is_custom_list', 'is_split_completed_list', 'status')
    entries = sgqlc.types.Field(sgqlc.types.list_of(MediaList), graphql_name='entries')
    name = sgqlc.types.Field(String, graphql_name='name')
    is_custom_list = sgqlc.types.Field(Boolean, graphql_name='isCustomList')
    is_split_completed_list = sgqlc.types.Field(Boolean, graphql_name='isSplitCompletedList')
    status = sgqlc.types.Field(MediaListStatus, graphql_name='status')


class MediaListOptions(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('score_format', 'row_order', 'use_legacy_lists', 'anime_list', 'manga_list', 'shared_theme', 'shared_theme_enabled')
    score_format = sgqlc.types.Field(ScoreFormat, graphql_name='scoreFormat')
    row_order = sgqlc.types.Field(String, graphql_name='rowOrder')
    use_legacy_lists = sgqlc.types.Field(Boolean, graphql_name='useLegacyLists')
    anime_list = sgqlc.types.Field('MediaListTypeOptions', graphql_name='animeList')
    manga_list = sgqlc.types.Field('MediaListTypeOptions', graphql_name='mangaList')
    shared_theme = sgqlc.types.Field(Json, graphql_name='sharedTheme')
    shared_theme_enabled = sgqlc.types.Field(Boolean, graphql_name='sharedThemeEnabled')


class MediaListTypeOptions(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('section_order', 'split_completed_section_by_format', 'theme', 'custom_lists', 'advanced_scoring', 'advanced_scoring_enabled')
    section_order = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='sectionOrder')
    split_completed_section_by_format = sgqlc.types.Field(Boolean, graphql_name='splitCompletedSectionByFormat')
    theme = sgqlc.types.Field(Json, graphql_name='theme')
    custom_lists = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='customLists')
    advanced_scoring = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='advancedScoring')
    advanced_scoring_enabled = sgqlc.types.Field(Boolean, graphql_name='advancedScoringEnabled')


class MediaMergeNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'type', 'media_id', 'deleted_media_titles', 'context', 'reason', 'created_at', 'media')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    deleted_media_titles = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='deletedMediaTitles')
    context = sgqlc.types.Field(String, graphql_name='context')
    reason = sgqlc.types.Field(String, graphql_name='reason')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    media = sgqlc.types.Field(Media, graphql_name='media')


class MediaRank(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'rank', 'type', 'format', 'year', 'season', 'all_time', 'context')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    rank = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='rank')
    type = sgqlc.types.Field(sgqlc.types.non_null(MediaRankType), graphql_name='type')
    format = sgqlc.types.Field(sgqlc.types.non_null(MediaFormat), graphql_name='format')
    year = sgqlc.types.Field(Int, graphql_name='year')
    season = sgqlc.types.Field(MediaSeason, graphql_name='season')
    all_time = sgqlc.types.Field(Boolean, graphql_name='allTime')
    context = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='context')


class MediaStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('score_distribution', 'status_distribution', 'airing_progression')
    score_distribution = sgqlc.types.Field(sgqlc.types.list_of('ScoreDistribution'), graphql_name='scoreDistribution')
    status_distribution = sgqlc.types.Field(sgqlc.types.list_of('StatusDistribution'), graphql_name='statusDistribution')
    airing_progression = sgqlc.types.Field(sgqlc.types.list_of(AiringProgression), graphql_name='airingProgression')


class MediaStreamingEpisode(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('title', 'thumbnail', 'url', 'site')
    title = sgqlc.types.Field(String, graphql_name='title')
    thumbnail = sgqlc.types.Field(String, graphql_name='thumbnail')
    url = sgqlc.types.Field(String, graphql_name='url')
    site = sgqlc.types.Field(String, graphql_name='site')


class MediaSubmission(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'submitter', 'assignee', 'status', 'submitter_stats', 'notes', 'source', 'changes', 'locked', 'media', 'submission', 'characters', 'staff', 'studios', 'relations', 'external_links', 'created_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    submitter = sgqlc.types.Field('User', graphql_name='submitter')
    assignee = sgqlc.types.Field('User', graphql_name='assignee')
    status = sgqlc.types.Field(SubmissionStatus, graphql_name='status')
    submitter_stats = sgqlc.types.Field(Json, graphql_name='submitterStats')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    source = sgqlc.types.Field(String, graphql_name='source')
    changes = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='changes')
    locked = sgqlc.types.Field(Boolean, graphql_name='locked')
    media = sgqlc.types.Field(Media, graphql_name='media')
    submission = sgqlc.types.Field(Media, graphql_name='submission')
    characters = sgqlc.types.Field(sgqlc.types.list_of('MediaSubmissionComparison'), graphql_name='characters')
    staff = sgqlc.types.Field(sgqlc.types.list_of('MediaSubmissionComparison'), graphql_name='staff')
    studios = sgqlc.types.Field(sgqlc.types.list_of('MediaSubmissionComparison'), graphql_name='studios')
    relations = sgqlc.types.Field(sgqlc.types.list_of(MediaEdge), graphql_name='relations')
    external_links = sgqlc.types.Field(sgqlc.types.list_of('MediaSubmissionComparison'), graphql_name='externalLinks')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')


class MediaSubmissionComparison(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('submission', 'character', 'staff', 'studio', 'external_link')
    submission = sgqlc.types.Field('MediaSubmissionEdge', graphql_name='submission')
    character = sgqlc.types.Field(MediaCharacter, graphql_name='character')
    staff = sgqlc.types.Field('StaffEdge', graphql_name='staff')
    studio = sgqlc.types.Field('StudioEdge', graphql_name='studio')
    external_link = sgqlc.types.Field(MediaExternalLink, graphql_name='externalLink')


class MediaSubmissionEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'character_role', 'staff_role', 'role_notes', 'dub_group', 'character_name', 'is_main', 'character', 'character_submission', 'voice_actor', 'voice_actor_submission', 'staff', 'staff_submission', 'studio', 'external_link', 'media')
    id = sgqlc.types.Field(Int, graphql_name='id')
    character_role = sgqlc.types.Field(CharacterRole, graphql_name='characterRole')
    staff_role = sgqlc.types.Field(String, graphql_name='staffRole')
    role_notes = sgqlc.types.Field(String, graphql_name='roleNotes')
    dub_group = sgqlc.types.Field(String, graphql_name='dubGroup')
    character_name = sgqlc.types.Field(String, graphql_name='characterName')
    is_main = sgqlc.types.Field(Boolean, graphql_name='isMain')
    character = sgqlc.types.Field(Character, graphql_name='character')
    character_submission = sgqlc.types.Field(Character, graphql_name='characterSubmission')
    voice_actor = sgqlc.types.Field('Staff', graphql_name='voiceActor')
    voice_actor_submission = sgqlc.types.Field('Staff', graphql_name='voiceActorSubmission')
    staff = sgqlc.types.Field('Staff', graphql_name='staff')
    staff_submission = sgqlc.types.Field('Staff', graphql_name='staffSubmission')
    studio = sgqlc.types.Field('Studio', graphql_name='studio')
    external_link = sgqlc.types.Field(MediaExternalLink, graphql_name='externalLink')
    media = sgqlc.types.Field(Media, graphql_name='media')


class MediaTag(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'name', 'description', 'category', 'rank', 'is_general_spoiler', 'is_media_spoiler', 'is_adult', 'user_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    category = sgqlc.types.Field(String, graphql_name='category')
    rank = sgqlc.types.Field(Int, graphql_name='rank')
    is_general_spoiler = sgqlc.types.Field(Boolean, graphql_name='isGeneralSpoiler')
    is_media_spoiler = sgqlc.types.Field(Boolean, graphql_name='isMediaSpoiler')
    is_adult = sgqlc.types.Field(Boolean, graphql_name='isAdult')
    user_id = sgqlc.types.Field(Int, graphql_name='userId')


class MediaTitle(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('romaji', 'english', 'native', 'user_preferred')
    romaji = sgqlc.types.Field(String, graphql_name='romaji', args=sgqlc.types.ArgDict((
        ('stylised', sgqlc.types.Arg(Boolean, graphql_name='stylised', default=None)),
))
    )
    english = sgqlc.types.Field(String, graphql_name='english', args=sgqlc.types.ArgDict((
        ('stylised', sgqlc.types.Arg(Boolean, graphql_name='stylised', default=None)),
))
    )
    native = sgqlc.types.Field(String, graphql_name='native', args=sgqlc.types.ArgDict((
        ('stylised', sgqlc.types.Arg(Boolean, graphql_name='stylised', default=None)),
))
    )
    user_preferred = sgqlc.types.Field(String, graphql_name='userPreferred')


class MediaTrailer(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'site', 'thumbnail')
    id = sgqlc.types.Field(String, graphql_name='id')
    site = sgqlc.types.Field(String, graphql_name='site')
    thumbnail = sgqlc.types.Field(String, graphql_name='thumbnail')


class MediaTrend(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('media_id', 'date', 'trending', 'average_score', 'popularity', 'in_progress', 'releasing', 'episode', 'media')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    date = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='date')
    trending = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='trending')
    average_score = sgqlc.types.Field(Int, graphql_name='averageScore')
    popularity = sgqlc.types.Field(Int, graphql_name='popularity')
    in_progress = sgqlc.types.Field(Int, graphql_name='inProgress')
    releasing = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='releasing')
    episode = sgqlc.types.Field(Int, graphql_name='episode')
    media = sgqlc.types.Field(Media, graphql_name='media')


class MediaTrendConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('MediaTrendEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(MediaTrend), graphql_name='nodes')
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')


class MediaTrendEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node',)
    node = sgqlc.types.Field(MediaTrend, graphql_name='node')


class MessageActivity(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'recipient_id', 'messenger_id', 'type', 'reply_count', 'message', 'is_locked', 'is_subscribed', 'like_count', 'is_liked', 'is_private', 'site_url', 'created_at', 'recipient', 'messenger', 'replies', 'likes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    recipient_id = sgqlc.types.Field(Int, graphql_name='recipientId')
    messenger_id = sgqlc.types.Field(Int, graphql_name='messengerId')
    type = sgqlc.types.Field(ActivityType, graphql_name='type')
    reply_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='replyCount')
    message = sgqlc.types.Field(String, graphql_name='message', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')
    is_subscribed = sgqlc.types.Field(Boolean, graphql_name='isSubscribed')
    like_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likeCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    is_private = sgqlc.types.Field(Boolean, graphql_name='isPrivate')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    recipient = sgqlc.types.Field('User', graphql_name='recipient')
    messenger = sgqlc.types.Field('User', graphql_name='messenger')
    replies = sgqlc.types.Field(sgqlc.types.list_of(ActivityReply), graphql_name='replies')
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes')


class ModAction(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user', 'mod', 'type', 'object_id', 'object_type', 'data', 'created_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user = sgqlc.types.Field('User', graphql_name='user')
    mod = sgqlc.types.Field('User', graphql_name='mod')
    type = sgqlc.types.Field(ModActionType, graphql_name='type')
    object_id = sgqlc.types.Field(Int, graphql_name='objectId')
    object_type = sgqlc.types.Field(String, graphql_name='objectType')
    data = sgqlc.types.Field(String, graphql_name='data')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')


class Mutation(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('update_user', 'save_media_list_entry', 'update_media_list_entries', 'delete_media_list_entry', 'delete_custom_list', 'save_text_activity', 'save_message_activity', 'save_list_activity', 'delete_activity', 'toggle_activity_pin', 'toggle_activity_subscription', 'save_activity_reply', 'delete_activity_reply', 'toggle_like', 'toggle_like_v2', 'toggle_follow', 'toggle_favourite', 'update_favourite_order', 'save_review', 'delete_review', 'rate_review', 'save_recommendation', 'save_thread', 'delete_thread', 'toggle_thread_subscription', 'save_thread_comment', 'delete_thread_comment', 'update_ani_chart_settings', 'update_ani_chart_highlights')
    update_user = sgqlc.types.Field('User', graphql_name='UpdateUser', args=sgqlc.types.ArgDict((
        ('about', sgqlc.types.Arg(String, graphql_name='about', default=None)),
        ('title_language', sgqlc.types.Arg(UserTitleLanguage, graphql_name='titleLanguage', default=None)),
        ('display_adult_content', sgqlc.types.Arg(Boolean, graphql_name='displayAdultContent', default=None)),
        ('airing_notifications', sgqlc.types.Arg(Boolean, graphql_name='airingNotifications', default=None)),
        ('score_format', sgqlc.types.Arg(ScoreFormat, graphql_name='scoreFormat', default=None)),
        ('row_order', sgqlc.types.Arg(String, graphql_name='rowOrder', default=None)),
        ('profile_color', sgqlc.types.Arg(String, graphql_name='profileColor', default=None)),
        ('donator_badge', sgqlc.types.Arg(String, graphql_name='donatorBadge', default=None)),
        ('notification_options', sgqlc.types.Arg(sgqlc.types.list_of(NotificationOptionInput), graphql_name='notificationOptions', default=None)),
        ('timezone', sgqlc.types.Arg(String, graphql_name='timezone', default=None)),
        ('activity_merge_time', sgqlc.types.Arg(Int, graphql_name='activityMergeTime', default=None)),
        ('anime_list_options', sgqlc.types.Arg(MediaListOptionsInput, graphql_name='animeListOptions', default=None)),
        ('manga_list_options', sgqlc.types.Arg(MediaListOptionsInput, graphql_name='mangaListOptions', default=None)),
        ('staff_name_language', sgqlc.types.Arg(UserStaffNameLanguage, graphql_name='staffNameLanguage', default=None)),
        ('restrict_messages_to_following', sgqlc.types.Arg(Boolean, graphql_name='restrictMessagesToFollowing', default=None)),
        ('disabled_list_activity', sgqlc.types.Arg(sgqlc.types.list_of(ListActivityOptionInput), graphql_name='disabledListActivity', default=None)),
))
    )
    save_media_list_entry = sgqlc.types.Field(MediaList, graphql_name='SaveMediaListEntry', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('status', sgqlc.types.Arg(MediaListStatus, graphql_name='status', default=None)),
        ('score', sgqlc.types.Arg(Float, graphql_name='score', default=None)),
        ('score_raw', sgqlc.types.Arg(Int, graphql_name='scoreRaw', default=None)),
        ('progress', sgqlc.types.Arg(Int, graphql_name='progress', default=None)),
        ('progress_volumes', sgqlc.types.Arg(Int, graphql_name='progressVolumes', default=None)),
        ('repeat', sgqlc.types.Arg(Int, graphql_name='repeat', default=None)),
        ('priority', sgqlc.types.Arg(Int, graphql_name='priority', default=None)),
        ('private', sgqlc.types.Arg(Boolean, graphql_name='private', default=None)),
        ('notes', sgqlc.types.Arg(String, graphql_name='notes', default=None)),
        ('hidden_from_status_lists', sgqlc.types.Arg(Boolean, graphql_name='hiddenFromStatusLists', default=None)),
        ('custom_lists', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='customLists', default=None)),
        ('advanced_scores', sgqlc.types.Arg(sgqlc.types.list_of(Float), graphql_name='advancedScores', default=None)),
        ('started_at', sgqlc.types.Arg(FuzzyDateInput, graphql_name='startedAt', default=None)),
        ('completed_at', sgqlc.types.Arg(FuzzyDateInput, graphql_name='completedAt', default=None)),
))
    )
    update_media_list_entries = sgqlc.types.Field(sgqlc.types.list_of(MediaList), graphql_name='UpdateMediaListEntries', args=sgqlc.types.ArgDict((
        ('status', sgqlc.types.Arg(MediaListStatus, graphql_name='status', default=None)),
        ('score', sgqlc.types.Arg(Float, graphql_name='score', default=None)),
        ('score_raw', sgqlc.types.Arg(Int, graphql_name='scoreRaw', default=None)),
        ('progress', sgqlc.types.Arg(Int, graphql_name='progress', default=None)),
        ('progress_volumes', sgqlc.types.Arg(Int, graphql_name='progressVolumes', default=None)),
        ('repeat', sgqlc.types.Arg(Int, graphql_name='repeat', default=None)),
        ('priority', sgqlc.types.Arg(Int, graphql_name='priority', default=None)),
        ('private', sgqlc.types.Arg(Boolean, graphql_name='private', default=None)),
        ('notes', sgqlc.types.Arg(String, graphql_name='notes', default=None)),
        ('hidden_from_status_lists', sgqlc.types.Arg(Boolean, graphql_name='hiddenFromStatusLists', default=None)),
        ('advanced_scores', sgqlc.types.Arg(sgqlc.types.list_of(Float), graphql_name='advancedScores', default=None)),
        ('started_at', sgqlc.types.Arg(FuzzyDateInput, graphql_name='startedAt', default=None)),
        ('completed_at', sgqlc.types.Arg(FuzzyDateInput, graphql_name='completedAt', default=None)),
        ('ids', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='ids', default=None)),
))
    )
    delete_media_list_entry = sgqlc.types.Field(Deleted, graphql_name='DeleteMediaListEntry', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
))
    )
    delete_custom_list = sgqlc.types.Field(Deleted, graphql_name='DeleteCustomList', args=sgqlc.types.ArgDict((
        ('custom_list', sgqlc.types.Arg(String, graphql_name='customList', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
))
    )
    save_text_activity = sgqlc.types.Field('TextActivity', graphql_name='SaveTextActivity', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('text', sgqlc.types.Arg(String, graphql_name='text', default=None)),
        ('locked', sgqlc.types.Arg(Boolean, graphql_name='locked', default=None)),
))
    )
    save_message_activity = sgqlc.types.Field(MessageActivity, graphql_name='SaveMessageActivity', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('message', sgqlc.types.Arg(String, graphql_name='message', default=None)),
        ('recipient_id', sgqlc.types.Arg(Int, graphql_name='recipientId', default=None)),
        ('private', sgqlc.types.Arg(Boolean, graphql_name='private', default=None)),
        ('locked', sgqlc.types.Arg(Boolean, graphql_name='locked', default=None)),
        ('as_mod', sgqlc.types.Arg(Boolean, graphql_name='asMod', default=None)),
))
    )
    save_list_activity = sgqlc.types.Field(ListActivity, graphql_name='SaveListActivity', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('locked', sgqlc.types.Arg(Boolean, graphql_name='locked', default=None)),
))
    )
    delete_activity = sgqlc.types.Field(Deleted, graphql_name='DeleteActivity', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
))
    )
    toggle_activity_pin = sgqlc.types.Field('ActivityUnion', graphql_name='ToggleActivityPin', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('pinned', sgqlc.types.Arg(Boolean, graphql_name='pinned', default=None)),
))
    )
    toggle_activity_subscription = sgqlc.types.Field('ActivityUnion', graphql_name='ToggleActivitySubscription', args=sgqlc.types.ArgDict((
        ('activity_id', sgqlc.types.Arg(Int, graphql_name='activityId', default=None)),
        ('subscribe', sgqlc.types.Arg(Boolean, graphql_name='subscribe', default=None)),
))
    )
    save_activity_reply = sgqlc.types.Field(ActivityReply, graphql_name='SaveActivityReply', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('activity_id', sgqlc.types.Arg(Int, graphql_name='activityId', default=None)),
        ('text', sgqlc.types.Arg(String, graphql_name='text', default=None)),
        ('as_mod', sgqlc.types.Arg(Boolean, graphql_name='asMod', default=None)),
))
    )
    delete_activity_reply = sgqlc.types.Field(Deleted, graphql_name='DeleteActivityReply', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
))
    )
    toggle_like = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='ToggleLike', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('type', sgqlc.types.Arg(LikeableType, graphql_name='type', default=None)),
))
    )
    toggle_like_v2 = sgqlc.types.Field('LikeableUnion', graphql_name='ToggleLikeV2', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('type', sgqlc.types.Arg(LikeableType, graphql_name='type', default=None)),
))
    )
    toggle_follow = sgqlc.types.Field('User', graphql_name='ToggleFollow', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
))
    )
    toggle_favourite = sgqlc.types.Field(Favourites, graphql_name='ToggleFavourite', args=sgqlc.types.ArgDict((
        ('anime_id', sgqlc.types.Arg(Int, graphql_name='animeId', default=None)),
        ('manga_id', sgqlc.types.Arg(Int, graphql_name='mangaId', default=None)),
        ('character_id', sgqlc.types.Arg(Int, graphql_name='characterId', default=None)),
        ('staff_id', sgqlc.types.Arg(Int, graphql_name='staffId', default=None)),
        ('studio_id', sgqlc.types.Arg(Int, graphql_name='studioId', default=None)),
))
    )
    update_favourite_order = sgqlc.types.Field(Favourites, graphql_name='UpdateFavouriteOrder', args=sgqlc.types.ArgDict((
        ('anime_ids', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='animeIds', default=None)),
        ('manga_ids', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mangaIds', default=None)),
        ('character_ids', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='characterIds', default=None)),
        ('staff_ids', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='staffIds', default=None)),
        ('studio_ids', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='studioIds', default=None)),
        ('anime_order', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='animeOrder', default=None)),
        ('manga_order', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mangaOrder', default=None)),
        ('character_order', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='characterOrder', default=None)),
        ('staff_order', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='staffOrder', default=None)),
        ('studio_order', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='studioOrder', default=None)),
))
    )
    save_review = sgqlc.types.Field('Review', graphql_name='SaveReview', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('body', sgqlc.types.Arg(String, graphql_name='body', default=None)),
        ('summary', sgqlc.types.Arg(String, graphql_name='summary', default=None)),
        ('score', sgqlc.types.Arg(Int, graphql_name='score', default=None)),
        ('private', sgqlc.types.Arg(Boolean, graphql_name='private', default=None)),
))
    )
    delete_review = sgqlc.types.Field(Deleted, graphql_name='DeleteReview', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
))
    )
    rate_review = sgqlc.types.Field('Review', graphql_name='RateReview', args=sgqlc.types.ArgDict((
        ('review_id', sgqlc.types.Arg(Int, graphql_name='reviewId', default=None)),
        ('rating', sgqlc.types.Arg(ReviewRating, graphql_name='rating', default=None)),
))
    )
    save_recommendation = sgqlc.types.Field('Recommendation', graphql_name='SaveRecommendation', args=sgqlc.types.ArgDict((
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('media_recommendation_id', sgqlc.types.Arg(Int, graphql_name='mediaRecommendationId', default=None)),
        ('rating', sgqlc.types.Arg(RecommendationRating, graphql_name='rating', default=None)),
))
    )
    save_thread = sgqlc.types.Field('Thread', graphql_name='SaveThread', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('title', sgqlc.types.Arg(String, graphql_name='title', default=None)),
        ('body', sgqlc.types.Arg(String, graphql_name='body', default=None)),
        ('categories', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='categories', default=None)),
        ('media_categories', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaCategories', default=None)),
        ('sticky', sgqlc.types.Arg(Boolean, graphql_name='sticky', default=None)),
        ('locked', sgqlc.types.Arg(Boolean, graphql_name='locked', default=None)),
))
    )
    delete_thread = sgqlc.types.Field(Deleted, graphql_name='DeleteThread', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
))
    )
    toggle_thread_subscription = sgqlc.types.Field('Thread', graphql_name='ToggleThreadSubscription', args=sgqlc.types.ArgDict((
        ('thread_id', sgqlc.types.Arg(Int, graphql_name='threadId', default=None)),
        ('subscribe', sgqlc.types.Arg(Boolean, graphql_name='subscribe', default=None)),
))
    )
    save_thread_comment = sgqlc.types.Field('ThreadComment', graphql_name='SaveThreadComment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('thread_id', sgqlc.types.Arg(Int, graphql_name='threadId', default=None)),
        ('parent_comment_id', sgqlc.types.Arg(Int, graphql_name='parentCommentId', default=None)),
        ('comment', sgqlc.types.Arg(String, graphql_name='comment', default=None)),
        ('locked', sgqlc.types.Arg(Boolean, graphql_name='locked', default=None)),
))
    )
    delete_thread_comment = sgqlc.types.Field(Deleted, graphql_name='DeleteThreadComment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
))
    )
    update_ani_chart_settings = sgqlc.types.Field(Json, graphql_name='UpdateAniChartSettings', args=sgqlc.types.ArgDict((
        ('title_language', sgqlc.types.Arg(String, graphql_name='titleLanguage', default=None)),
        ('outgoing_link_provider', sgqlc.types.Arg(String, graphql_name='outgoingLinkProvider', default=None)),
        ('theme', sgqlc.types.Arg(String, graphql_name='theme', default=None)),
        ('sort', sgqlc.types.Arg(String, graphql_name='sort', default=None)),
))
    )
    update_ani_chart_highlights = sgqlc.types.Field(Json, graphql_name='UpdateAniChartHighlights', args=sgqlc.types.ArgDict((
        ('highlights', sgqlc.types.Arg(sgqlc.types.list_of(AniChartHighlightInput), graphql_name='highlights', default=None)),
))
    )


class NotificationOption(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('type', 'enabled')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    enabled = sgqlc.types.Field(Boolean, graphql_name='enabled')


class Page(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('page_info', 'users', 'media', 'characters', 'staff', 'studios', 'media_list', 'airing_schedules', 'media_trends', 'notifications', 'followers', 'following', 'activities', 'activity_replies', 'threads', 'thread_comments', 'reviews', 'recommendations', 'likes')
    page_info = sgqlc.types.Field('PageInfo', graphql_name='pageInfo')
    users = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='users', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('is_moderator', sgqlc.types.Arg(Boolean, graphql_name='isModerator', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    media = sgqlc.types.Field(sgqlc.types.list_of(Media), graphql_name='media', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('id_mal', sgqlc.types.Arg(Int, graphql_name='idMal', default=None)),
        ('start_date', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate', default=None)),
        ('end_date', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate', default=None)),
        ('season', sgqlc.types.Arg(MediaSeason, graphql_name='season', default=None)),
        ('season_year', sgqlc.types.Arg(Int, graphql_name='seasonYear', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('format', sgqlc.types.Arg(MediaFormat, graphql_name='format', default=None)),
        ('status', sgqlc.types.Arg(MediaStatus, graphql_name='status', default=None)),
        ('episodes', sgqlc.types.Arg(Int, graphql_name='episodes', default=None)),
        ('duration', sgqlc.types.Arg(Int, graphql_name='duration', default=None)),
        ('chapters', sgqlc.types.Arg(Int, graphql_name='chapters', default=None)),
        ('volumes', sgqlc.types.Arg(Int, graphql_name='volumes', default=None)),
        ('is_adult', sgqlc.types.Arg(Boolean, graphql_name='isAdult', default=None)),
        ('genre', sgqlc.types.Arg(String, graphql_name='genre', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('minimum_tag_rank', sgqlc.types.Arg(Int, graphql_name='minimumTagRank', default=None)),
        ('tag_category', sgqlc.types.Arg(String, graphql_name='tagCategory', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('licensed_by', sgqlc.types.Arg(String, graphql_name='licensedBy', default=None)),
        ('licensed_by_id', sgqlc.types.Arg(Int, graphql_name='licensedById', default=None)),
        ('average_score', sgqlc.types.Arg(Int, graphql_name='averageScore', default=None)),
        ('popularity', sgqlc.types.Arg(Int, graphql_name='popularity', default=None)),
        ('source', sgqlc.types.Arg(MediaSource, graphql_name='source', default=None)),
        ('country_of_origin', sgqlc.types.Arg(CountryCode, graphql_name='countryOfOrigin', default=None)),
        ('is_licensed', sgqlc.types.Arg(Boolean, graphql_name='isLicensed', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('id_mal_not', sgqlc.types.Arg(Int, graphql_name='idMal_not', default=None)),
        ('id_mal_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='idMal_in', default=None)),
        ('id_mal_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='idMal_not_in', default=None)),
        ('start_date_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate_greater', default=None)),
        ('start_date_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate_lesser', default=None)),
        ('start_date_like', sgqlc.types.Arg(String, graphql_name='startDate_like', default=None)),
        ('end_date_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate_greater', default=None)),
        ('end_date_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate_lesser', default=None)),
        ('end_date_like', sgqlc.types.Arg(String, graphql_name='endDate_like', default=None)),
        ('format_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaFormat), graphql_name='format_in', default=None)),
        ('format_not', sgqlc.types.Arg(MediaFormat, graphql_name='format_not', default=None)),
        ('format_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaFormat), graphql_name='format_not_in', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaStatus), graphql_name='status_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaStatus, graphql_name='status_not', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaStatus), graphql_name='status_not_in', default=None)),
        ('episodes_greater', sgqlc.types.Arg(Int, graphql_name='episodes_greater', default=None)),
        ('episodes_lesser', sgqlc.types.Arg(Int, graphql_name='episodes_lesser', default=None)),
        ('duration_greater', sgqlc.types.Arg(Int, graphql_name='duration_greater', default=None)),
        ('duration_lesser', sgqlc.types.Arg(Int, graphql_name='duration_lesser', default=None)),
        ('chapters_greater', sgqlc.types.Arg(Int, graphql_name='chapters_greater', default=None)),
        ('chapters_lesser', sgqlc.types.Arg(Int, graphql_name='chapters_lesser', default=None)),
        ('volumes_greater', sgqlc.types.Arg(Int, graphql_name='volumes_greater', default=None)),
        ('volumes_lesser', sgqlc.types.Arg(Int, graphql_name='volumes_lesser', default=None)),
        ('genre_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='genre_in', default=None)),
        ('genre_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='genre_not_in', default=None)),
        ('tag_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tag_in', default=None)),
        ('tag_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tag_not_in', default=None)),
        ('tag_category_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tagCategory_in', default=None)),
        ('tag_category_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tagCategory_not_in', default=None)),
        ('licensed_by_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='licensedBy_in', default=None)),
        ('licensed_by_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='licensedById_in', default=None)),
        ('average_score_not', sgqlc.types.Arg(Int, graphql_name='averageScore_not', default=None)),
        ('average_score_greater', sgqlc.types.Arg(Int, graphql_name='averageScore_greater', default=None)),
        ('average_score_lesser', sgqlc.types.Arg(Int, graphql_name='averageScore_lesser', default=None)),
        ('popularity_not', sgqlc.types.Arg(Int, graphql_name='popularity_not', default=None)),
        ('popularity_greater', sgqlc.types.Arg(Int, graphql_name='popularity_greater', default=None)),
        ('popularity_lesser', sgqlc.types.Arg(Int, graphql_name='popularity_lesser', default=None)),
        ('source_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaSource), graphql_name='source_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
))
    )
    characters = sgqlc.types.Field(sgqlc.types.list_of(Character), graphql_name='characters', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('is_birthday', sgqlc.types.Arg(Boolean, graphql_name='isBirthday', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(CharacterSort), graphql_name='sort', default=None)),
))
    )
    staff = sgqlc.types.Field(sgqlc.types.list_of('Staff'), graphql_name='staff', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('is_birthday', sgqlc.types.Arg(Boolean, graphql_name='isBirthday', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    studios = sgqlc.types.Field(sgqlc.types.list_of('Studio'), graphql_name='studios', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StudioSort), graphql_name='sort', default=None)),
))
    )
    media_list = sgqlc.types.Field(sgqlc.types.list_of(MediaList), graphql_name='mediaList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('user_name', sgqlc.types.Arg(String, graphql_name='userName', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('status', sgqlc.types.Arg(MediaListStatus, graphql_name='status', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('is_following', sgqlc.types.Arg(Boolean, graphql_name='isFollowing', default=None)),
        ('notes', sgqlc.types.Arg(String, graphql_name='notes', default=None)),
        ('started_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt', default=None)),
        ('completed_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt', default=None)),
        ('compare_with_auth_list', sgqlc.types.Arg(Boolean, graphql_name='compareWithAuthList', default=None)),
        ('user_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_in', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_in', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_not_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaListStatus, graphql_name='status_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('notes_like', sgqlc.types.Arg(String, graphql_name='notes_like', default=None)),
        ('started_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_greater', default=None)),
        ('started_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_lesser', default=None)),
        ('started_at_like', sgqlc.types.Arg(String, graphql_name='startedAt_like', default=None)),
        ('completed_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_greater', default=None)),
        ('completed_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_lesser', default=None)),
        ('completed_at_like', sgqlc.types.Arg(String, graphql_name='completedAt_like', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaListSort), graphql_name='sort', default=None)),
))
    )
    airing_schedules = sgqlc.types.Field(sgqlc.types.list_of(AiringSchedule), graphql_name='airingSchedules', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('episode', sgqlc.types.Arg(Int, graphql_name='episode', default=None)),
        ('airing_at', sgqlc.types.Arg(Int, graphql_name='airingAt', default=None)),
        ('not_yet_aired', sgqlc.types.Arg(Boolean, graphql_name='notYetAired', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('episode_not', sgqlc.types.Arg(Int, graphql_name='episode_not', default=None)),
        ('episode_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='episode_in', default=None)),
        ('episode_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='episode_not_in', default=None)),
        ('episode_greater', sgqlc.types.Arg(Int, graphql_name='episode_greater', default=None)),
        ('episode_lesser', sgqlc.types.Arg(Int, graphql_name='episode_lesser', default=None)),
        ('airing_at_greater', sgqlc.types.Arg(Int, graphql_name='airingAt_greater', default=None)),
        ('airing_at_lesser', sgqlc.types.Arg(Int, graphql_name='airingAt_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(AiringSort), graphql_name='sort', default=None)),
))
    )
    media_trends = sgqlc.types.Field(sgqlc.types.list_of(MediaTrend), graphql_name='mediaTrends', args=sgqlc.types.ArgDict((
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('date', sgqlc.types.Arg(Int, graphql_name='date', default=None)),
        ('trending', sgqlc.types.Arg(Int, graphql_name='trending', default=None)),
        ('average_score', sgqlc.types.Arg(Int, graphql_name='averageScore', default=None)),
        ('popularity', sgqlc.types.Arg(Int, graphql_name='popularity', default=None)),
        ('episode', sgqlc.types.Arg(Int, graphql_name='episode', default=None)),
        ('releasing', sgqlc.types.Arg(Boolean, graphql_name='releasing', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('date_greater', sgqlc.types.Arg(Int, graphql_name='date_greater', default=None)),
        ('date_lesser', sgqlc.types.Arg(Int, graphql_name='date_lesser', default=None)),
        ('trending_greater', sgqlc.types.Arg(Int, graphql_name='trending_greater', default=None)),
        ('trending_lesser', sgqlc.types.Arg(Int, graphql_name='trending_lesser', default=None)),
        ('trending_not', sgqlc.types.Arg(Int, graphql_name='trending_not', default=None)),
        ('average_score_greater', sgqlc.types.Arg(Int, graphql_name='averageScore_greater', default=None)),
        ('average_score_lesser', sgqlc.types.Arg(Int, graphql_name='averageScore_lesser', default=None)),
        ('average_score_not', sgqlc.types.Arg(Int, graphql_name='averageScore_not', default=None)),
        ('popularity_greater', sgqlc.types.Arg(Int, graphql_name='popularity_greater', default=None)),
        ('popularity_lesser', sgqlc.types.Arg(Int, graphql_name='popularity_lesser', default=None)),
        ('popularity_not', sgqlc.types.Arg(Int, graphql_name='popularity_not', default=None)),
        ('episode_greater', sgqlc.types.Arg(Int, graphql_name='episode_greater', default=None)),
        ('episode_lesser', sgqlc.types.Arg(Int, graphql_name='episode_lesser', default=None)),
        ('episode_not', sgqlc.types.Arg(Int, graphql_name='episode_not', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaTrendSort), graphql_name='sort', default=None)),
))
    )
    notifications = sgqlc.types.Field(sgqlc.types.list_of('NotificationUnion'), graphql_name='notifications', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(NotificationType, graphql_name='type', default=None)),
        ('reset_notification_count', sgqlc.types.Arg(Boolean, graphql_name='resetNotificationCount', default=None)),
        ('type_in', sgqlc.types.Arg(sgqlc.types.list_of(NotificationType), graphql_name='type_in', default=None)),
))
    )
    followers = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='followers', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    following = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='following', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    activities = sgqlc.types.Field(sgqlc.types.list_of('ActivityUnion'), graphql_name='activities', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('messenger_id', sgqlc.types.Arg(Int, graphql_name='messengerId', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('type', sgqlc.types.Arg(ActivityType, graphql_name='type', default=None)),
        ('is_following', sgqlc.types.Arg(Boolean, graphql_name='isFollowing', default=None)),
        ('has_replies', sgqlc.types.Arg(Boolean, graphql_name='hasReplies', default=None)),
        ('has_replies_or_type_text', sgqlc.types.Arg(Boolean, graphql_name='hasRepliesOrTypeText', default=None)),
        ('created_at', sgqlc.types.Arg(Int, graphql_name='createdAt', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('user_id_not', sgqlc.types.Arg(Int, graphql_name='userId_not', default=None)),
        ('user_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_in', default=None)),
        ('user_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_not_in', default=None)),
        ('messenger_id_not', sgqlc.types.Arg(Int, graphql_name='messengerId_not', default=None)),
        ('messenger_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='messengerId_in', default=None)),
        ('messenger_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='messengerId_not_in', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('type_not', sgqlc.types.Arg(ActivityType, graphql_name='type_not', default=None)),
        ('type_in', sgqlc.types.Arg(sgqlc.types.list_of(ActivityType), graphql_name='type_in', default=None)),
        ('type_not_in', sgqlc.types.Arg(sgqlc.types.list_of(ActivityType), graphql_name='type_not_in', default=None)),
        ('created_at_greater', sgqlc.types.Arg(Int, graphql_name='createdAt_greater', default=None)),
        ('created_at_lesser', sgqlc.types.Arg(Int, graphql_name='createdAt_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ActivitySort), graphql_name='sort', default=None)),
))
    )
    activity_replies = sgqlc.types.Field(sgqlc.types.list_of(ActivityReply), graphql_name='activityReplies', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('activity_id', sgqlc.types.Arg(Int, graphql_name='activityId', default=None)),
))
    )
    threads = sgqlc.types.Field(sgqlc.types.list_of('Thread'), graphql_name='threads', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('reply_user_id', sgqlc.types.Arg(Int, graphql_name='replyUserId', default=None)),
        ('subscribed', sgqlc.types.Arg(Boolean, graphql_name='subscribed', default=None)),
        ('category_id', sgqlc.types.Arg(Int, graphql_name='categoryId', default=None)),
        ('media_category_id', sgqlc.types.Arg(Int, graphql_name='mediaCategoryId', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ThreadSort), graphql_name='sort', default=None)),
))
    )
    thread_comments = sgqlc.types.Field(sgqlc.types.list_of('ThreadComment'), graphql_name='threadComments', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('thread_id', sgqlc.types.Arg(Int, graphql_name='threadId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ThreadCommentSort), graphql_name='sort', default=None)),
))
    )
    reviews = sgqlc.types.Field(sgqlc.types.list_of('Review'), graphql_name='reviews', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('media_type', sgqlc.types.Arg(MediaType, graphql_name='mediaType', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ReviewSort), graphql_name='sort', default=None)),
))
    )
    recommendations = sgqlc.types.Field(sgqlc.types.list_of('Recommendation'), graphql_name='recommendations', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('media_recommendation_id', sgqlc.types.Arg(Int, graphql_name='mediaRecommendationId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('rating', sgqlc.types.Arg(Int, graphql_name='rating', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('rating_greater', sgqlc.types.Arg(Int, graphql_name='rating_greater', default=None)),
        ('rating_lesser', sgqlc.types.Arg(Int, graphql_name='rating_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(RecommendationSort), graphql_name='sort', default=None)),
))
    )
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes', args=sgqlc.types.ArgDict((
        ('likeable_id', sgqlc.types.Arg(Int, graphql_name='likeableId', default=None)),
        ('type', sgqlc.types.Arg(LikeableType, graphql_name='type', default=None)),
))
    )


class PageInfo(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('total', 'per_page', 'current_page', 'last_page', 'has_next_page')
    total = sgqlc.types.Field(Int, graphql_name='total')
    per_page = sgqlc.types.Field(Int, graphql_name='perPage')
    current_page = sgqlc.types.Field(Int, graphql_name='currentPage')
    last_page = sgqlc.types.Field(Int, graphql_name='lastPage')
    has_next_page = sgqlc.types.Field(Boolean, graphql_name='hasNextPage')


class ParsedMarkdown(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('html',)
    html = sgqlc.types.Field(String, graphql_name='html')


class Query(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('page', 'media', 'media_trend', 'airing_schedule', 'character', 'staff', 'media_list', 'media_list_collection', 'genre_collection', 'media_tag_collection', 'user', 'viewer', 'notification', 'studio', 'review', 'activity', 'activity_reply', 'following', 'follower', 'thread', 'thread_comment', 'recommendation', 'like', 'markdown', 'ani_chart_user', 'site_statistics', 'external_link_source_collection')
    page = sgqlc.types.Field('Page', graphql_name='Page', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    media = sgqlc.types.Field('Media', graphql_name='Media', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('id_mal', sgqlc.types.Arg(Int, graphql_name='idMal', default=None)),
        ('start_date', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate', default=None)),
        ('end_date', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate', default=None)),
        ('season', sgqlc.types.Arg(MediaSeason, graphql_name='season', default=None)),
        ('season_year', sgqlc.types.Arg(Int, graphql_name='seasonYear', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('format', sgqlc.types.Arg(MediaFormat, graphql_name='format', default=None)),
        ('status', sgqlc.types.Arg(MediaStatus, graphql_name='status', default=None)),
        ('episodes', sgqlc.types.Arg(Int, graphql_name='episodes', default=None)),
        ('duration', sgqlc.types.Arg(Int, graphql_name='duration', default=None)),
        ('chapters', sgqlc.types.Arg(Int, graphql_name='chapters', default=None)),
        ('volumes', sgqlc.types.Arg(Int, graphql_name='volumes', default=None)),
        ('is_adult', sgqlc.types.Arg(Boolean, graphql_name='isAdult', default=None)),
        ('genre', sgqlc.types.Arg(String, graphql_name='genre', default=None)),
        ('tag', sgqlc.types.Arg(String, graphql_name='tag', default=None)),
        ('minimum_tag_rank', sgqlc.types.Arg(Int, graphql_name='minimumTagRank', default=None)),
        ('tag_category', sgqlc.types.Arg(String, graphql_name='tagCategory', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('licensed_by', sgqlc.types.Arg(String, graphql_name='licensedBy', default=None)),
        ('licensed_by_id', sgqlc.types.Arg(Int, graphql_name='licensedById', default=None)),
        ('average_score', sgqlc.types.Arg(Int, graphql_name='averageScore', default=None)),
        ('popularity', sgqlc.types.Arg(Int, graphql_name='popularity', default=None)),
        ('source', sgqlc.types.Arg(MediaSource, graphql_name='source', default=None)),
        ('country_of_origin', sgqlc.types.Arg(CountryCode, graphql_name='countryOfOrigin', default=None)),
        ('is_licensed', sgqlc.types.Arg(Boolean, graphql_name='isLicensed', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('id_mal_not', sgqlc.types.Arg(Int, graphql_name='idMal_not', default=None)),
        ('id_mal_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='idMal_in', default=None)),
        ('id_mal_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='idMal_not_in', default=None)),
        ('start_date_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate_greater', default=None)),
        ('start_date_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startDate_lesser', default=None)),
        ('start_date_like', sgqlc.types.Arg(String, graphql_name='startDate_like', default=None)),
        ('end_date_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate_greater', default=None)),
        ('end_date_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='endDate_lesser', default=None)),
        ('end_date_like', sgqlc.types.Arg(String, graphql_name='endDate_like', default=None)),
        ('format_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaFormat), graphql_name='format_in', default=None)),
        ('format_not', sgqlc.types.Arg(MediaFormat, graphql_name='format_not', default=None)),
        ('format_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaFormat), graphql_name='format_not_in', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaStatus), graphql_name='status_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaStatus, graphql_name='status_not', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaStatus), graphql_name='status_not_in', default=None)),
        ('episodes_greater', sgqlc.types.Arg(Int, graphql_name='episodes_greater', default=None)),
        ('episodes_lesser', sgqlc.types.Arg(Int, graphql_name='episodes_lesser', default=None)),
        ('duration_greater', sgqlc.types.Arg(Int, graphql_name='duration_greater', default=None)),
        ('duration_lesser', sgqlc.types.Arg(Int, graphql_name='duration_lesser', default=None)),
        ('chapters_greater', sgqlc.types.Arg(Int, graphql_name='chapters_greater', default=None)),
        ('chapters_lesser', sgqlc.types.Arg(Int, graphql_name='chapters_lesser', default=None)),
        ('volumes_greater', sgqlc.types.Arg(Int, graphql_name='volumes_greater', default=None)),
        ('volumes_lesser', sgqlc.types.Arg(Int, graphql_name='volumes_lesser', default=None)),
        ('genre_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='genre_in', default=None)),
        ('genre_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='genre_not_in', default=None)),
        ('tag_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tag_in', default=None)),
        ('tag_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tag_not_in', default=None)),
        ('tag_category_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tagCategory_in', default=None)),
        ('tag_category_not_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='tagCategory_not_in', default=None)),
        ('licensed_by_in', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='licensedBy_in', default=None)),
        ('licensed_by_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='licensedById_in', default=None)),
        ('average_score_not', sgqlc.types.Arg(Int, graphql_name='averageScore_not', default=None)),
        ('average_score_greater', sgqlc.types.Arg(Int, graphql_name='averageScore_greater', default=None)),
        ('average_score_lesser', sgqlc.types.Arg(Int, graphql_name='averageScore_lesser', default=None)),
        ('popularity_not', sgqlc.types.Arg(Int, graphql_name='popularity_not', default=None)),
        ('popularity_greater', sgqlc.types.Arg(Int, graphql_name='popularity_greater', default=None)),
        ('popularity_lesser', sgqlc.types.Arg(Int, graphql_name='popularity_lesser', default=None)),
        ('source_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaSource), graphql_name='source_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
))
    )
    media_trend = sgqlc.types.Field('MediaTrend', graphql_name='MediaTrend', args=sgqlc.types.ArgDict((
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('date', sgqlc.types.Arg(Int, graphql_name='date', default=None)),
        ('trending', sgqlc.types.Arg(Int, graphql_name='trending', default=None)),
        ('average_score', sgqlc.types.Arg(Int, graphql_name='averageScore', default=None)),
        ('popularity', sgqlc.types.Arg(Int, graphql_name='popularity', default=None)),
        ('episode', sgqlc.types.Arg(Int, graphql_name='episode', default=None)),
        ('releasing', sgqlc.types.Arg(Boolean, graphql_name='releasing', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('date_greater', sgqlc.types.Arg(Int, graphql_name='date_greater', default=None)),
        ('date_lesser', sgqlc.types.Arg(Int, graphql_name='date_lesser', default=None)),
        ('trending_greater', sgqlc.types.Arg(Int, graphql_name='trending_greater', default=None)),
        ('trending_lesser', sgqlc.types.Arg(Int, graphql_name='trending_lesser', default=None)),
        ('trending_not', sgqlc.types.Arg(Int, graphql_name='trending_not', default=None)),
        ('average_score_greater', sgqlc.types.Arg(Int, graphql_name='averageScore_greater', default=None)),
        ('average_score_lesser', sgqlc.types.Arg(Int, graphql_name='averageScore_lesser', default=None)),
        ('average_score_not', sgqlc.types.Arg(Int, graphql_name='averageScore_not', default=None)),
        ('popularity_greater', sgqlc.types.Arg(Int, graphql_name='popularity_greater', default=None)),
        ('popularity_lesser', sgqlc.types.Arg(Int, graphql_name='popularity_lesser', default=None)),
        ('popularity_not', sgqlc.types.Arg(Int, graphql_name='popularity_not', default=None)),
        ('episode_greater', sgqlc.types.Arg(Int, graphql_name='episode_greater', default=None)),
        ('episode_lesser', sgqlc.types.Arg(Int, graphql_name='episode_lesser', default=None)),
        ('episode_not', sgqlc.types.Arg(Int, graphql_name='episode_not', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaTrendSort), graphql_name='sort', default=None)),
))
    )
    airing_schedule = sgqlc.types.Field('AiringSchedule', graphql_name='AiringSchedule', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('episode', sgqlc.types.Arg(Int, graphql_name='episode', default=None)),
        ('airing_at', sgqlc.types.Arg(Int, graphql_name='airingAt', default=None)),
        ('not_yet_aired', sgqlc.types.Arg(Boolean, graphql_name='notYetAired', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('episode_not', sgqlc.types.Arg(Int, graphql_name='episode_not', default=None)),
        ('episode_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='episode_in', default=None)),
        ('episode_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='episode_not_in', default=None)),
        ('episode_greater', sgqlc.types.Arg(Int, graphql_name='episode_greater', default=None)),
        ('episode_lesser', sgqlc.types.Arg(Int, graphql_name='episode_lesser', default=None)),
        ('airing_at_greater', sgqlc.types.Arg(Int, graphql_name='airingAt_greater', default=None)),
        ('airing_at_lesser', sgqlc.types.Arg(Int, graphql_name='airingAt_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(AiringSort), graphql_name='sort', default=None)),
))
    )
    character = sgqlc.types.Field('Character', graphql_name='Character', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('is_birthday', sgqlc.types.Arg(Boolean, graphql_name='isBirthday', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(CharacterSort), graphql_name='sort', default=None)),
))
    )
    staff = sgqlc.types.Field('Staff', graphql_name='Staff', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('is_birthday', sgqlc.types.Arg(Boolean, graphql_name='isBirthday', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StaffSort), graphql_name='sort', default=None)),
))
    )
    media_list = sgqlc.types.Field('MediaList', graphql_name='MediaList', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('user_name', sgqlc.types.Arg(String, graphql_name='userName', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('status', sgqlc.types.Arg(MediaListStatus, graphql_name='status', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('is_following', sgqlc.types.Arg(Boolean, graphql_name='isFollowing', default=None)),
        ('notes', sgqlc.types.Arg(String, graphql_name='notes', default=None)),
        ('started_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt', default=None)),
        ('completed_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt', default=None)),
        ('compare_with_auth_list', sgqlc.types.Arg(Boolean, graphql_name='compareWithAuthList', default=None)),
        ('user_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_in', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_in', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_not_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaListStatus, graphql_name='status_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('notes_like', sgqlc.types.Arg(String, graphql_name='notes_like', default=None)),
        ('started_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_greater', default=None)),
        ('started_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_lesser', default=None)),
        ('started_at_like', sgqlc.types.Arg(String, graphql_name='startedAt_like', default=None)),
        ('completed_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_greater', default=None)),
        ('completed_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_lesser', default=None)),
        ('completed_at_like', sgqlc.types.Arg(String, graphql_name='completedAt_like', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaListSort), graphql_name='sort', default=None)),
))
    )
    media_list_collection = sgqlc.types.Field('MediaListCollection', graphql_name='MediaListCollection', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('user_name', sgqlc.types.Arg(String, graphql_name='userName', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('status', sgqlc.types.Arg(MediaListStatus, graphql_name='status', default=None)),
        ('notes', sgqlc.types.Arg(String, graphql_name='notes', default=None)),
        ('started_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt', default=None)),
        ('completed_at', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt', default=None)),
        ('force_single_completed_list', sgqlc.types.Arg(Boolean, graphql_name='forceSingleCompletedList', default=None)),
        ('chunk', sgqlc.types.Arg(Int, graphql_name='chunk', default=None)),
        ('per_chunk', sgqlc.types.Arg(Int, graphql_name='perChunk', default=None)),
        ('status_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_in', default=None)),
        ('status_not_in', sgqlc.types.Arg(sgqlc.types.list_of(MediaListStatus), graphql_name='status_not_in', default=None)),
        ('status_not', sgqlc.types.Arg(MediaListStatus, graphql_name='status_not', default=None)),
        ('notes_like', sgqlc.types.Arg(String, graphql_name='notes_like', default=None)),
        ('started_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_greater', default=None)),
        ('started_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='startedAt_lesser', default=None)),
        ('started_at_like', sgqlc.types.Arg(String, graphql_name='startedAt_like', default=None)),
        ('completed_at_greater', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_greater', default=None)),
        ('completed_at_lesser', sgqlc.types.Arg(FuzzyDateInt, graphql_name='completedAt_lesser', default=None)),
        ('completed_at_like', sgqlc.types.Arg(String, graphql_name='completedAt_like', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaListSort), graphql_name='sort', default=None)),
))
    )
    genre_collection = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='GenreCollection')
    media_tag_collection = sgqlc.types.Field(sgqlc.types.list_of(MediaTag), graphql_name='MediaTagCollection', args=sgqlc.types.ArgDict((
        ('status', sgqlc.types.Arg(Int, graphql_name='status', default=None)),
))
    )
    user = sgqlc.types.Field('User', graphql_name='User', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('is_moderator', sgqlc.types.Arg(Boolean, graphql_name='isModerator', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    viewer = sgqlc.types.Field('User', graphql_name='Viewer')
    notification = sgqlc.types.Field('NotificationUnion', graphql_name='Notification', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(NotificationType, graphql_name='type', default=None)),
        ('reset_notification_count', sgqlc.types.Arg(Boolean, graphql_name='resetNotificationCount', default=None)),
        ('type_in', sgqlc.types.Arg(sgqlc.types.list_of(NotificationType), graphql_name='type_in', default=None)),
))
    )
    studio = sgqlc.types.Field('Studio', graphql_name='Studio', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(StudioSort), graphql_name='sort', default=None)),
))
    )
    review = sgqlc.types.Field('Review', graphql_name='Review', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('media_type', sgqlc.types.Arg(MediaType, graphql_name='mediaType', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ReviewSort), graphql_name='sort', default=None)),
))
    )
    activity = sgqlc.types.Field('ActivityUnion', graphql_name='Activity', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('messenger_id', sgqlc.types.Arg(Int, graphql_name='messengerId', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('type', sgqlc.types.Arg(ActivityType, graphql_name='type', default=None)),
        ('is_following', sgqlc.types.Arg(Boolean, graphql_name='isFollowing', default=None)),
        ('has_replies', sgqlc.types.Arg(Boolean, graphql_name='hasReplies', default=None)),
        ('has_replies_or_type_text', sgqlc.types.Arg(Boolean, graphql_name='hasRepliesOrTypeText', default=None)),
        ('created_at', sgqlc.types.Arg(Int, graphql_name='createdAt', default=None)),
        ('id_not', sgqlc.types.Arg(Int, graphql_name='id_not', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_not_in', default=None)),
        ('user_id_not', sgqlc.types.Arg(Int, graphql_name='userId_not', default=None)),
        ('user_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_in', default=None)),
        ('user_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='userId_not_in', default=None)),
        ('messenger_id_not', sgqlc.types.Arg(Int, graphql_name='messengerId_not', default=None)),
        ('messenger_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='messengerId_in', default=None)),
        ('messenger_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='messengerId_not_in', default=None)),
        ('media_id_not', sgqlc.types.Arg(Int, graphql_name='mediaId_not', default=None)),
        ('media_id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_in', default=None)),
        ('media_id_not_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='mediaId_not_in', default=None)),
        ('type_not', sgqlc.types.Arg(ActivityType, graphql_name='type_not', default=None)),
        ('type_in', sgqlc.types.Arg(sgqlc.types.list_of(ActivityType), graphql_name='type_in', default=None)),
        ('type_not_in', sgqlc.types.Arg(sgqlc.types.list_of(ActivityType), graphql_name='type_not_in', default=None)),
        ('created_at_greater', sgqlc.types.Arg(Int, graphql_name='createdAt_greater', default=None)),
        ('created_at_lesser', sgqlc.types.Arg(Int, graphql_name='createdAt_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ActivitySort), graphql_name='sort', default=None)),
))
    )
    activity_reply = sgqlc.types.Field('ActivityReply', graphql_name='ActivityReply', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('activity_id', sgqlc.types.Arg(Int, graphql_name='activityId', default=None)),
))
    )
    following = sgqlc.types.Field('User', graphql_name='Following', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    follower = sgqlc.types.Field('User', graphql_name='Follower', args=sgqlc.types.ArgDict((
        ('user_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserSort), graphql_name='sort', default=None)),
))
    )
    thread = sgqlc.types.Field('Thread', graphql_name='Thread', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('reply_user_id', sgqlc.types.Arg(Int, graphql_name='replyUserId', default=None)),
        ('subscribed', sgqlc.types.Arg(Boolean, graphql_name='subscribed', default=None)),
        ('category_id', sgqlc.types.Arg(Int, graphql_name='categoryId', default=None)),
        ('media_category_id', sgqlc.types.Arg(Int, graphql_name='mediaCategoryId', default=None)),
        ('search', sgqlc.types.Arg(String, graphql_name='search', default=None)),
        ('id_in', sgqlc.types.Arg(sgqlc.types.list_of(Int), graphql_name='id_in', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ThreadSort), graphql_name='sort', default=None)),
))
    )
    thread_comment = sgqlc.types.Field(sgqlc.types.list_of('ThreadComment'), graphql_name='ThreadComment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('thread_id', sgqlc.types.Arg(Int, graphql_name='threadId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(ThreadCommentSort), graphql_name='sort', default=None)),
))
    )
    recommendation = sgqlc.types.Field('Recommendation', graphql_name='Recommendation', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('media_id', sgqlc.types.Arg(Int, graphql_name='mediaId', default=None)),
        ('media_recommendation_id', sgqlc.types.Arg(Int, graphql_name='mediaRecommendationId', default=None)),
        ('user_id', sgqlc.types.Arg(Int, graphql_name='userId', default=None)),
        ('rating', sgqlc.types.Arg(Int, graphql_name='rating', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('rating_greater', sgqlc.types.Arg(Int, graphql_name='rating_greater', default=None)),
        ('rating_lesser', sgqlc.types.Arg(Int, graphql_name='rating_lesser', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(RecommendationSort), graphql_name='sort', default=None)),
))
    )
    like = sgqlc.types.Field('User', graphql_name='Like', args=sgqlc.types.ArgDict((
        ('likeable_id', sgqlc.types.Arg(Int, graphql_name='likeableId', default=None)),
        ('type', sgqlc.types.Arg(LikeableType, graphql_name='type', default=None)),
))
    )
    markdown = sgqlc.types.Field(ParsedMarkdown, graphql_name='Markdown', args=sgqlc.types.ArgDict((
        ('markdown', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='markdown', default=None)),
))
    )
    ani_chart_user = sgqlc.types.Field('AniChartUser', graphql_name='AniChartUser')
    site_statistics = sgqlc.types.Field('SiteStatistics', graphql_name='SiteStatistics')
    external_link_source_collection = sgqlc.types.Field(sgqlc.types.list_of(MediaExternalLink), graphql_name='ExternalLinkSourceCollection', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Int, graphql_name='id', default=None)),
        ('type', sgqlc.types.Arg(ExternalLinkType, graphql_name='type', default=None)),
        ('media_type', sgqlc.types.Arg(ExternalLinkMediaType, graphql_name='mediaType', default=None)),
))
    )


class Recommendation(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'rating', 'user_rating', 'media', 'media_recommendation', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    rating = sgqlc.types.Field(Int, graphql_name='rating')
    user_rating = sgqlc.types.Field(RecommendationRating, graphql_name='userRating')
    media = sgqlc.types.Field(Media, graphql_name='media')
    media_recommendation = sgqlc.types.Field(Media, graphql_name='mediaRecommendation')
    user = sgqlc.types.Field('User', graphql_name='user')


class RecommendationConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('RecommendationEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Recommendation), graphql_name='nodes')
    page_info = sgqlc.types.Field(PageInfo, graphql_name='pageInfo')


class RecommendationEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node',)
    node = sgqlc.types.Field(Recommendation, graphql_name='node')


class RelatedMediaAdditionNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'type', 'media_id', 'context', 'created_at', 'media')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    media = sgqlc.types.Field(Media, graphql_name='media')


class Report(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'reporter', 'reported', 'reason', 'created_at', 'cleared')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    reporter = sgqlc.types.Field('User', graphql_name='reporter')
    reported = sgqlc.types.Field('User', graphql_name='reported')
    reason = sgqlc.types.Field(String, graphql_name='reason')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    cleared = sgqlc.types.Field(Boolean, graphql_name='cleared')


class Review(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'media_id', 'media_type', 'summary', 'body', 'rating', 'rating_amount', 'user_rating', 'score', 'private', 'site_url', 'created_at', 'updated_at', 'user', 'media')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    media_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='mediaId')
    media_type = sgqlc.types.Field(MediaType, graphql_name='mediaType')
    summary = sgqlc.types.Field(String, graphql_name='summary')
    body = sgqlc.types.Field(String, graphql_name='body', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    rating = sgqlc.types.Field(Int, graphql_name='rating')
    rating_amount = sgqlc.types.Field(Int, graphql_name='ratingAmount')
    user_rating = sgqlc.types.Field(ReviewRating, graphql_name='userRating')
    score = sgqlc.types.Field(Int, graphql_name='score')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='updatedAt')
    user = sgqlc.types.Field('User', graphql_name='user')
    media = sgqlc.types.Field(Media, graphql_name='media')


class ReviewConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('ReviewEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Review), graphql_name='nodes')
    page_info = sgqlc.types.Field(PageInfo, graphql_name='pageInfo')


class ReviewEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node',)
    node = sgqlc.types.Field(Review, graphql_name='node')


class RevisionHistory(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'action', 'changes', 'user', 'media', 'character', 'staff', 'studio', 'external_link', 'created_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    action = sgqlc.types.Field(RevisionHistoryAction, graphql_name='action')
    changes = sgqlc.types.Field(Json, graphql_name='changes')
    user = sgqlc.types.Field('User', graphql_name='user')
    media = sgqlc.types.Field(Media, graphql_name='media')
    character = sgqlc.types.Field(Character, graphql_name='character')
    staff = sgqlc.types.Field('Staff', graphql_name='staff')
    studio = sgqlc.types.Field('Studio', graphql_name='studio')
    external_link = sgqlc.types.Field(MediaExternalLink, graphql_name='externalLink')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')


class ScoreDistribution(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('score', 'amount')
    score = sgqlc.types.Field(Int, graphql_name='score')
    amount = sgqlc.types.Field(Int, graphql_name='amount')


class SiteStatistics(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('users', 'anime', 'manga', 'characters', 'staff', 'studios', 'reviews')
    users = sgqlc.types.Field('SiteTrendConnection', graphql_name='users', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    anime = sgqlc.types.Field('SiteTrendConnection', graphql_name='anime', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    manga = sgqlc.types.Field('SiteTrendConnection', graphql_name='manga', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    characters = sgqlc.types.Field('SiteTrendConnection', graphql_name='characters', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    staff = sgqlc.types.Field('SiteTrendConnection', graphql_name='staff', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    studios = sgqlc.types.Field('SiteTrendConnection', graphql_name='studios', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    reviews = sgqlc.types.Field('SiteTrendConnection', graphql_name='reviews', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(SiteTrendSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )


class SiteTrend(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('date', 'count', 'change')
    date = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='date')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    change = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='change')


class SiteTrendConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('SiteTrendEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(SiteTrend), graphql_name='nodes')
    page_info = sgqlc.types.Field(PageInfo, graphql_name='pageInfo')


class SiteTrendEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node',)
    node = sgqlc.types.Field(SiteTrend, graphql_name='node')


class Staff(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'name', 'language', 'language_v2', 'image', 'description', 'primary_occupations', 'gender', 'date_of_birth', 'date_of_death', 'age', 'years_active', 'home_town', 'blood_type', 'is_favourite', 'is_favourite_blocked', 'site_url', 'staff_media', 'characters', 'character_media', 'updated_at', 'staff', 'submitter', 'submission_status', 'submission_notes', 'favourites', 'mod_notes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    name = sgqlc.types.Field('StaffName', graphql_name='name')
    language = sgqlc.types.Field(StaffLanguage, graphql_name='language')
    language_v2 = sgqlc.types.Field(String, graphql_name='languageV2')
    image = sgqlc.types.Field('StaffImage', graphql_name='image')
    description = sgqlc.types.Field(String, graphql_name='description', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    primary_occupations = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='primaryOccupations')
    gender = sgqlc.types.Field(String, graphql_name='gender')
    date_of_birth = sgqlc.types.Field(FuzzyDate, graphql_name='dateOfBirth')
    date_of_death = sgqlc.types.Field(FuzzyDate, graphql_name='dateOfDeath')
    age = sgqlc.types.Field(Int, graphql_name='age')
    years_active = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='yearsActive')
    home_town = sgqlc.types.Field(String, graphql_name='homeTown')
    blood_type = sgqlc.types.Field(String, graphql_name='bloodType')
    is_favourite = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavourite')
    is_favourite_blocked = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavouriteBlocked')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    staff_media = sgqlc.types.Field(MediaConnection, graphql_name='staffMedia', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
        ('type', sgqlc.types.Arg(MediaType, graphql_name='type', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    characters = sgqlc.types.Field(CharacterConnection, graphql_name='characters', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(CharacterSort), graphql_name='sort', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    character_media = sgqlc.types.Field(MediaConnection, graphql_name='characterMedia', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    updated_at = sgqlc.types.Field(Int, graphql_name='updatedAt')
    staff = sgqlc.types.Field('Staff', graphql_name='staff')
    submitter = sgqlc.types.Field('User', graphql_name='submitter')
    submission_status = sgqlc.types.Field(Int, graphql_name='submissionStatus')
    submission_notes = sgqlc.types.Field(String, graphql_name='submissionNotes')
    favourites = sgqlc.types.Field(Int, graphql_name='favourites')
    mod_notes = sgqlc.types.Field(String, graphql_name='modNotes')


class StaffConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('StaffEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Staff), graphql_name='nodes')
    page_info = sgqlc.types.Field(PageInfo, graphql_name='pageInfo')


class StaffEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node', 'id', 'role', 'favourite_order')
    node = sgqlc.types.Field(Staff, graphql_name='node')
    id = sgqlc.types.Field(Int, graphql_name='id')
    role = sgqlc.types.Field(String, graphql_name='role')
    favourite_order = sgqlc.types.Field(Int, graphql_name='favouriteOrder')


class StaffImage(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('large', 'medium')
    large = sgqlc.types.Field(String, graphql_name='large')
    medium = sgqlc.types.Field(String, graphql_name='medium')


class StaffName(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('first', 'middle', 'last', 'full', 'native', 'alternative', 'user_preferred')
    first = sgqlc.types.Field(String, graphql_name='first')
    middle = sgqlc.types.Field(String, graphql_name='middle')
    last = sgqlc.types.Field(String, graphql_name='last')
    full = sgqlc.types.Field(String, graphql_name='full')
    native = sgqlc.types.Field(String, graphql_name='native')
    alternative = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alternative')
    user_preferred = sgqlc.types.Field(String, graphql_name='userPreferred')


class StaffRoleType(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('voice_actor', 'role_notes', 'dub_group')
    voice_actor = sgqlc.types.Field(Staff, graphql_name='voiceActor')
    role_notes = sgqlc.types.Field(String, graphql_name='roleNotes')
    dub_group = sgqlc.types.Field(String, graphql_name='dubGroup')


class StaffStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('staff', 'amount', 'mean_score', 'time_watched')
    staff = sgqlc.types.Field(Staff, graphql_name='staff')
    amount = sgqlc.types.Field(Int, graphql_name='amount')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')
    time_watched = sgqlc.types.Field(Int, graphql_name='timeWatched')


class StaffSubmission(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'staff', 'submission', 'submitter', 'assignee', 'status', 'notes', 'source', 'locked', 'created_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    staff = sgqlc.types.Field(Staff, graphql_name='staff')
    submission = sgqlc.types.Field(Staff, graphql_name='submission')
    submitter = sgqlc.types.Field('User', graphql_name='submitter')
    assignee = sgqlc.types.Field('User', graphql_name='assignee')
    status = sgqlc.types.Field(SubmissionStatus, graphql_name='status')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    source = sgqlc.types.Field(String, graphql_name='source')
    locked = sgqlc.types.Field(Boolean, graphql_name='locked')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')


class StatusDistribution(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('status', 'amount')
    status = sgqlc.types.Field(MediaListStatus, graphql_name='status')
    amount = sgqlc.types.Field(Int, graphql_name='amount')


class Studio(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'name', 'is_animation_studio', 'media', 'site_url', 'is_favourite', 'favourites')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    is_animation_studio = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isAnimationStudio')
    media = sgqlc.types.Field(MediaConnection, graphql_name='media', args=sgqlc.types.ArgDict((
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(MediaSort), graphql_name='sort', default=None)),
        ('is_main', sgqlc.types.Arg(Boolean, graphql_name='isMain', default=None)),
        ('on_list', sgqlc.types.Arg(Boolean, graphql_name='onList', default=None)),
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
        ('per_page', sgqlc.types.Arg(Int, graphql_name='perPage', default=None)),
))
    )
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    is_favourite = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavourite')
    favourites = sgqlc.types.Field(Int, graphql_name='favourites')


class StudioConnection(sgqlc.types.relay.Connection):
    __schema__ = anilist_schema
    __field_names__ = ('edges', 'nodes', 'page_info')
    edges = sgqlc.types.Field(sgqlc.types.list_of('StudioEdge'), graphql_name='edges')
    nodes = sgqlc.types.Field(sgqlc.types.list_of(Studio), graphql_name='nodes')
    page_info = sgqlc.types.Field(PageInfo, graphql_name='pageInfo')


class StudioEdge(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('node', 'id', 'is_main', 'favourite_order')
    node = sgqlc.types.Field(Studio, graphql_name='node')
    id = sgqlc.types.Field(Int, graphql_name='id')
    is_main = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isMain')
    favourite_order = sgqlc.types.Field(Int, graphql_name='favouriteOrder')


class StudioStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('studio', 'amount', 'mean_score', 'time_watched')
    studio = sgqlc.types.Field(Studio, graphql_name='studio')
    amount = sgqlc.types.Field(Int, graphql_name='amount')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')
    time_watched = sgqlc.types.Field(Int, graphql_name='timeWatched')


class TagStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('tag', 'amount', 'mean_score', 'time_watched')
    tag = sgqlc.types.Field(MediaTag, graphql_name='tag')
    amount = sgqlc.types.Field(Int, graphql_name='amount')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')
    time_watched = sgqlc.types.Field(Int, graphql_name='timeWatched')


class TextActivity(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'reply_count', 'text', 'site_url', 'is_locked', 'is_subscribed', 'like_count', 'is_liked', 'is_pinned', 'created_at', 'user', 'replies', 'likes')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(Int, graphql_name='userId')
    type = sgqlc.types.Field(ActivityType, graphql_name='type')
    reply_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='replyCount')
    text = sgqlc.types.Field(String, graphql_name='text', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')
    is_subscribed = sgqlc.types.Field(Boolean, graphql_name='isSubscribed')
    like_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likeCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    is_pinned = sgqlc.types.Field(Boolean, graphql_name='isPinned')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    user = sgqlc.types.Field('User', graphql_name='user')
    replies = sgqlc.types.Field(sgqlc.types.list_of(ActivityReply), graphql_name='replies')
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes')


class Thread(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'title', 'body', 'user_id', 'reply_user_id', 'reply_comment_id', 'reply_count', 'view_count', 'is_locked', 'is_sticky', 'is_subscribed', 'like_count', 'is_liked', 'replied_at', 'created_at', 'updated_at', 'user', 'reply_user', 'likes', 'site_url', 'categories', 'media_categories')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    body = sgqlc.types.Field(String, graphql_name='body', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    reply_user_id = sgqlc.types.Field(Int, graphql_name='replyUserId')
    reply_comment_id = sgqlc.types.Field(Int, graphql_name='replyCommentId')
    reply_count = sgqlc.types.Field(Int, graphql_name='replyCount')
    view_count = sgqlc.types.Field(Int, graphql_name='viewCount')
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')
    is_sticky = sgqlc.types.Field(Boolean, graphql_name='isSticky')
    is_subscribed = sgqlc.types.Field(Boolean, graphql_name='isSubscribed')
    like_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likeCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    replied_at = sgqlc.types.Field(Int, graphql_name='repliedAt')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='updatedAt')
    user = sgqlc.types.Field('User', graphql_name='user')
    reply_user = sgqlc.types.Field('User', graphql_name='replyUser')
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    categories = sgqlc.types.Field(sgqlc.types.list_of('ThreadCategory'), graphql_name='categories')
    media_categories = sgqlc.types.Field(sgqlc.types.list_of(Media), graphql_name='mediaCategories')


class ThreadCategory(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class ThreadComment(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'thread_id', 'comment', 'like_count', 'is_liked', 'site_url', 'created_at', 'updated_at', 'thread', 'user', 'likes', 'child_comments', 'is_locked')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(Int, graphql_name='userId')
    thread_id = sgqlc.types.Field(Int, graphql_name='threadId')
    comment = sgqlc.types.Field(String, graphql_name='comment', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    like_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='likeCount')
    is_liked = sgqlc.types.Field(Boolean, graphql_name='isLiked')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='updatedAt')
    thread = sgqlc.types.Field(Thread, graphql_name='thread')
    user = sgqlc.types.Field('User', graphql_name='user')
    likes = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='likes')
    child_comments = sgqlc.types.Field(Json, graphql_name='childComments')
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')


class ThreadCommentLikeNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'comment_id', 'context', 'created_at', 'thread', 'comment', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    comment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    thread = sgqlc.types.Field(Thread, graphql_name='thread')
    comment = sgqlc.types.Field(ThreadComment, graphql_name='comment')
    user = sgqlc.types.Field('User', graphql_name='user')


class ThreadCommentMentionNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'comment_id', 'context', 'created_at', 'thread', 'comment', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    comment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    thread = sgqlc.types.Field(Thread, graphql_name='thread')
    comment = sgqlc.types.Field(ThreadComment, graphql_name='comment')
    user = sgqlc.types.Field('User', graphql_name='user')


class ThreadCommentReplyNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'comment_id', 'context', 'created_at', 'thread', 'comment', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    comment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    thread = sgqlc.types.Field(Thread, graphql_name='thread')
    comment = sgqlc.types.Field(ThreadComment, graphql_name='comment')
    user = sgqlc.types.Field('User', graphql_name='user')


class ThreadCommentSubscribedNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'comment_id', 'context', 'created_at', 'thread', 'comment', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    comment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='commentId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    thread = sgqlc.types.Field(Thread, graphql_name='thread')
    comment = sgqlc.types.Field(ThreadComment, graphql_name='comment')
    user = sgqlc.types.Field('User', graphql_name='user')


class ThreadLikeNotification(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'user_id', 'type', 'thread_id', 'context', 'created_at', 'thread', 'comment', 'user')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='userId')
    type = sgqlc.types.Field(NotificationType, graphql_name='type')
    thread_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='threadId')
    context = sgqlc.types.Field(String, graphql_name='context')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    thread = sgqlc.types.Field(Thread, graphql_name='thread')
    comment = sgqlc.types.Field(ThreadComment, graphql_name='comment')
    user = sgqlc.types.Field('User', graphql_name='user')


class User(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('id', 'name', 'about', 'avatar', 'banner_image', 'is_following', 'is_follower', 'is_blocked', 'bans', 'options', 'media_list_options', 'favourites', 'statistics', 'unread_notification_count', 'site_url', 'donator_tier', 'donator_badge', 'moderator_roles', 'created_at', 'updated_at', 'stats', 'moderator_status', 'previous_names')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    about = sgqlc.types.Field(String, graphql_name='about', args=sgqlc.types.ArgDict((
        ('as_html', sgqlc.types.Arg(Boolean, graphql_name='asHtml', default=None)),
))
    )
    avatar = sgqlc.types.Field('UserAvatar', graphql_name='avatar')
    banner_image = sgqlc.types.Field(String, graphql_name='bannerImage')
    is_following = sgqlc.types.Field(Boolean, graphql_name='isFollowing')
    is_follower = sgqlc.types.Field(Boolean, graphql_name='isFollower')
    is_blocked = sgqlc.types.Field(Boolean, graphql_name='isBlocked')
    bans = sgqlc.types.Field(Json, graphql_name='bans')
    options = sgqlc.types.Field('UserOptions', graphql_name='options')
    media_list_options = sgqlc.types.Field(MediaListOptions, graphql_name='mediaListOptions')
    favourites = sgqlc.types.Field(Favourites, graphql_name='favourites', args=sgqlc.types.ArgDict((
        ('page', sgqlc.types.Arg(Int, graphql_name='page', default=None)),
))
    )
    statistics = sgqlc.types.Field('UserStatisticTypes', graphql_name='statistics')
    unread_notification_count = sgqlc.types.Field(Int, graphql_name='unreadNotificationCount')
    site_url = sgqlc.types.Field(String, graphql_name='siteUrl')
    donator_tier = sgqlc.types.Field(Int, graphql_name='donatorTier')
    donator_badge = sgqlc.types.Field(String, graphql_name='donatorBadge')
    moderator_roles = sgqlc.types.Field(sgqlc.types.list_of(ModRole), graphql_name='moderatorRoles')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(Int, graphql_name='updatedAt')
    stats = sgqlc.types.Field('UserStats', graphql_name='stats')
    moderator_status = sgqlc.types.Field(String, graphql_name='moderatorStatus')
    previous_names = sgqlc.types.Field(sgqlc.types.list_of('UserPreviousName'), graphql_name='previousNames')


class UserActivityHistory(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('date', 'amount', 'level')
    date = sgqlc.types.Field(Int, graphql_name='date')
    amount = sgqlc.types.Field(Int, graphql_name='amount')
    level = sgqlc.types.Field(Int, graphql_name='level')


class UserAvatar(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('large', 'medium')
    large = sgqlc.types.Field(String, graphql_name='large')
    medium = sgqlc.types.Field(String, graphql_name='medium')


class UserCountryStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'country')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    country = sgqlc.types.Field(CountryCode, graphql_name='country')


class UserFormatStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'format')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    format = sgqlc.types.Field(MediaFormat, graphql_name='format')


class UserGenreStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'genre')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    genre = sgqlc.types.Field(String, graphql_name='genre')


class UserLengthStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'length')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    length = sgqlc.types.Field(String, graphql_name='length')


class UserModData(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('alts', 'bans', 'ip', 'counts', 'privacy', 'email')
    alts = sgqlc.types.Field(sgqlc.types.list_of(User), graphql_name='alts')
    bans = sgqlc.types.Field(Json, graphql_name='bans')
    ip = sgqlc.types.Field(Json, graphql_name='ip')
    counts = sgqlc.types.Field(Json, graphql_name='counts')
    privacy = sgqlc.types.Field(Int, graphql_name='privacy')
    email = sgqlc.types.Field(String, graphql_name='email')


class UserOptions(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('title_language', 'display_adult_content', 'airing_notifications', 'profile_color', 'notification_options', 'timezone', 'activity_merge_time', 'staff_name_language', 'restrict_messages_to_following', 'disabled_list_activity')
    title_language = sgqlc.types.Field(UserTitleLanguage, graphql_name='titleLanguage')
    display_adult_content = sgqlc.types.Field(Boolean, graphql_name='displayAdultContent')
    airing_notifications = sgqlc.types.Field(Boolean, graphql_name='airingNotifications')
    profile_color = sgqlc.types.Field(String, graphql_name='profileColor')
    notification_options = sgqlc.types.Field(sgqlc.types.list_of(NotificationOption), graphql_name='notificationOptions')
    timezone = sgqlc.types.Field(String, graphql_name='timezone')
    activity_merge_time = sgqlc.types.Field(Int, graphql_name='activityMergeTime')
    staff_name_language = sgqlc.types.Field(UserStaffNameLanguage, graphql_name='staffNameLanguage')
    restrict_messages_to_following = sgqlc.types.Field(Boolean, graphql_name='restrictMessagesToFollowing')
    disabled_list_activity = sgqlc.types.Field(sgqlc.types.list_of(ListActivityOption), graphql_name='disabledListActivity')


class UserPreviousName(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('name', 'created_at', 'updated_at')
    name = sgqlc.types.Field(String, graphql_name='name')
    created_at = sgqlc.types.Field(Int, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(Int, graphql_name='updatedAt')


class UserReleaseYearStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'release_year')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    release_year = sgqlc.types.Field(Int, graphql_name='releaseYear')


class UserScoreStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'score')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    score = sgqlc.types.Field(Int, graphql_name='score')


class UserStaffStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'staff')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    staff = sgqlc.types.Field(Staff, graphql_name='staff')


class UserStartYearStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'start_year')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    start_year = sgqlc.types.Field(Int, graphql_name='startYear')


class UserStatisticTypes(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('anime', 'manga')
    anime = sgqlc.types.Field('UserStatistics', graphql_name='anime')
    manga = sgqlc.types.Field('UserStatistics', graphql_name='manga')


class UserStatistics(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'standard_deviation', 'minutes_watched', 'episodes_watched', 'chapters_read', 'volumes_read', 'formats', 'statuses', 'scores', 'lengths', 'release_years', 'start_years', 'genres', 'tags', 'countries', 'voice_actors', 'staff', 'studios')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    standard_deviation = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='standardDeviation')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    episodes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='episodesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    volumes_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='volumesRead')
    formats = sgqlc.types.Field(sgqlc.types.list_of(UserFormatStatistic), graphql_name='formats', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    statuses = sgqlc.types.Field(sgqlc.types.list_of('UserStatusStatistic'), graphql_name='statuses', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    scores = sgqlc.types.Field(sgqlc.types.list_of(UserScoreStatistic), graphql_name='scores', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    lengths = sgqlc.types.Field(sgqlc.types.list_of(UserLengthStatistic), graphql_name='lengths', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    release_years = sgqlc.types.Field(sgqlc.types.list_of(UserReleaseYearStatistic), graphql_name='releaseYears', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    start_years = sgqlc.types.Field(sgqlc.types.list_of(UserStartYearStatistic), graphql_name='startYears', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    genres = sgqlc.types.Field(sgqlc.types.list_of(UserGenreStatistic), graphql_name='genres', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of('UserTagStatistic'), graphql_name='tags', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    countries = sgqlc.types.Field(sgqlc.types.list_of(UserCountryStatistic), graphql_name='countries', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    voice_actors = sgqlc.types.Field(sgqlc.types.list_of('UserVoiceActorStatistic'), graphql_name='voiceActors', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    staff = sgqlc.types.Field(sgqlc.types.list_of(UserStaffStatistic), graphql_name='staff', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )
    studios = sgqlc.types.Field(sgqlc.types.list_of('UserStudioStatistic'), graphql_name='studios', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('sort', sgqlc.types.Arg(sgqlc.types.list_of(UserStatisticsSort), graphql_name='sort', default=None)),
))
    )


class UserStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('watched_time', 'chapters_read', 'activity_history', 'anime_status_distribution', 'manga_status_distribution', 'anime_score_distribution', 'manga_score_distribution', 'anime_list_scores', 'manga_list_scores', 'favoured_genres_overview', 'favoured_genres', 'favoured_tags', 'favoured_actors', 'favoured_staff', 'favoured_studios', 'favoured_years', 'favoured_formats')
    watched_time = sgqlc.types.Field(Int, graphql_name='watchedTime')
    chapters_read = sgqlc.types.Field(Int, graphql_name='chaptersRead')
    activity_history = sgqlc.types.Field(sgqlc.types.list_of(UserActivityHistory), graphql_name='activityHistory')
    anime_status_distribution = sgqlc.types.Field(sgqlc.types.list_of(StatusDistribution), graphql_name='animeStatusDistribution')
    manga_status_distribution = sgqlc.types.Field(sgqlc.types.list_of(StatusDistribution), graphql_name='mangaStatusDistribution')
    anime_score_distribution = sgqlc.types.Field(sgqlc.types.list_of(ScoreDistribution), graphql_name='animeScoreDistribution')
    manga_score_distribution = sgqlc.types.Field(sgqlc.types.list_of(ScoreDistribution), graphql_name='mangaScoreDistribution')
    anime_list_scores = sgqlc.types.Field(ListScoreStats, graphql_name='animeListScores')
    manga_list_scores = sgqlc.types.Field(ListScoreStats, graphql_name='mangaListScores')
    favoured_genres_overview = sgqlc.types.Field(sgqlc.types.list_of(GenreStats), graphql_name='favouredGenresOverview')
    favoured_genres = sgqlc.types.Field(sgqlc.types.list_of(GenreStats), graphql_name='favouredGenres')
    favoured_tags = sgqlc.types.Field(sgqlc.types.list_of(TagStats), graphql_name='favouredTags')
    favoured_actors = sgqlc.types.Field(sgqlc.types.list_of(StaffStats), graphql_name='favouredActors')
    favoured_staff = sgqlc.types.Field(sgqlc.types.list_of(StaffStats), graphql_name='favouredStaff')
    favoured_studios = sgqlc.types.Field(sgqlc.types.list_of(StudioStats), graphql_name='favouredStudios')
    favoured_years = sgqlc.types.Field(sgqlc.types.list_of('YearStats'), graphql_name='favouredYears')
    favoured_formats = sgqlc.types.Field(sgqlc.types.list_of(FormatStats), graphql_name='favouredFormats')


class UserStatusStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'status')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    status = sgqlc.types.Field(MediaListStatus, graphql_name='status')


class UserStudioStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'studio')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    studio = sgqlc.types.Field(Studio, graphql_name='studio')


class UserTagStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'tag')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    tag = sgqlc.types.Field(MediaTag, graphql_name='tag')


class UserVoiceActorStatistic(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('count', 'mean_score', 'minutes_watched', 'chapters_read', 'media_ids', 'voice_actor', 'character_ids')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')
    mean_score = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='meanScore')
    minutes_watched = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minutesWatched')
    chapters_read = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='chaptersRead')
    media_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='mediaIds')
    voice_actor = sgqlc.types.Field(Staff, graphql_name='voiceActor')
    character_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Int)), graphql_name='characterIds')


class YearStats(sgqlc.types.Type):
    __schema__ = anilist_schema
    __field_names__ = ('year', 'amount', 'mean_score')
    year = sgqlc.types.Field(Int, graphql_name='year')
    amount = sgqlc.types.Field(Int, graphql_name='amount')
    mean_score = sgqlc.types.Field(Int, graphql_name='meanScore')



########################################################################
# Unions
########################################################################
class ActivityUnion(sgqlc.types.Union):
    __schema__ = anilist_schema
    __types__ = (TextActivity, ListActivity, MessageActivity)


class LikeableUnion(sgqlc.types.Union):
    __schema__ = anilist_schema
    __types__ = (ListActivity, TextActivity, MessageActivity, ActivityReply, Thread, ThreadComment)


class NotificationUnion(sgqlc.types.Union):
    __schema__ = anilist_schema
    __types__ = (AiringNotification, FollowingNotification, ActivityMessageNotification, ActivityMentionNotification, ActivityReplyNotification, ActivityReplySubscribedNotification, ActivityLikeNotification, ActivityReplyLikeNotification, ThreadCommentMentionNotification, ThreadCommentReplyNotification, ThreadCommentSubscribedNotification, ThreadCommentLikeNotification, ThreadLikeNotification, RelatedMediaAdditionNotification, MediaDataChangeNotification, MediaMergeNotification, MediaDeletionNotification)



########################################################################
# Schema Entry Points
########################################################################
anilist_schema.query_type = Query
anilist_schema.mutation_type = Mutation
anilist_schema.subscription_type = None

