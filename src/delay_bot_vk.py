from datetime import timedelta
import requests

from vk_api import (
    VkApi,
)
from vk_api.longpoll import (
    VkLongPoll,
    VkEventType,
)
from vk_api.utils import (
    get_random_id,
)

from config_parser import (
    token,
)
from date_features import (
    get_moscow_time_week_day,
    check_message_day_time,
)
from helpers import (
    get_relevant_message,
)
from pytz import (
    UTC,
)

vk_session = VkApi(token=token)

pm_lp = VkLongPoll(vk_session)
vk = vk_session.get_api()

ALERTED = {}

try:
    for event in pm_lp.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg_time, msg_day = get_moscow_time_week_day(event.timestamp)
            need_message = check_message_day_time(msg_time, msg_day)
            user_id = event.user_id
            is_alerted = ALERTED.get(user_id, None)
            print(msg_time, msg_day, sep='___')
            print('ALERTED', ALERTED)
            print('is_alerted', is_alerted)
            if is_alerted and msg_day == is_alerted[1] and msg_time - is_alerted[0] <= timedelta(hours=8):
                print('his alerted')
                need_message = False

            if need_message:
                vk.messages.send(
                    user_id=user_id,
                    message=get_relevant_message(msg_day),
                    random_id=get_random_id())
                ALERTED[user_id] = [msg_time, msg_day]
except requests.exceptions.Timeout:
    pass

