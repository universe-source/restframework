"""
    Configure
"""


class Config(object):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_UNKNOWN = 'U'
    GENDERS = (
        (GENDER_MALE, u'男'),
        (GENDER_FEMALE, u'女'),
        (GENDER_UNKNOWN, u'未知'),
    )

    SESSION_KEY = 'personid'

    # 评价
    SCORE_BEGIN = 1
    SCORE_1 = SCORE_BEGIN
    SCORE_2 = 2
    SCORE_3 = 3
    SCORE_4 = 4
    SCORE_5 = 5
    SCORE_END = SCORE_5
    SCORES = (
        (SCORE_1, u'1星'),
        (SCORE_2, u'2星'),
        (SCORE_3, u'3星'),
        (SCORE_4, u'4星'),
        (SCORE_5, u'5星'),
    )

    # 留言板类型(工单, 或者其他)
    REPLY_TICKET = 'ticket'
    REPLY_BLOG = 'blog'
    REPLYS = (
        (REPLY_TICKET, u'工单对话'),
        (REPLY_BLOG, u'博客对话'),
    )

    # 工单状态
    TICKET_STATUS_CREATED = 'created'
    TICKET_STATUS_ACCEPTED = 'accepted'
    TICKET_STATUS_HANDLED = 'handled'
    TICKET_STATUS_CONFIRMED = 'confirmed'
    TICKET_STATUS_SCORED = 'scored'
    TICKET_STATUS_CLOSED = 'closed'
    TICKET_STATUSES = (
        (TICKET_STATUS_CREATED, u'已创建'),
        (TICKET_STATUS_ACCEPTED, u'已受理'),
        (TICKET_STATUS_HANDLED, u'已处理'),
        (TICKET_STATUS_CONFIRMED, u'已确认'),
        (TICKET_STATUS_SCORED, u'已评价'),
        (TICKET_STATUS_CLOSED, u'已关闭'),
    )
