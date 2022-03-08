import imp
import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class VkBot:
    @staticmethod
    def create_keyboard(matrix, color=VkKeyboardColor.PRIMARY):
        keyboard = VkKeyboard(one_time=True)
        for list in matrix:
            for e in list:
                keyboard.add_button(e, color)
            keyboard.add_line()
        keyboard.lines.pop()
        return keyboard

    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token = token)
        self.vk = self.vk_session.get_api()

    def send_msg(self, id, text, keyboard=VkKeyboard.get_empty_keyboard()):
        self.vk.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message=text,
            keyboard=keyboard
        )
    

