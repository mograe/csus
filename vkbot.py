from distutils.command.upload import upload
import imp
import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import requests
from io import BytesIO

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
    
    def send_msg_with_pic(self, id, text, url, keyboard=VkKeyboard.get_empty_keyboard()):
        img = requests.get(url).content
        f = BytesIO(img)
        upload = vk_api.VkUpload(self.vk)
        photo = upload.photo_messages(f)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.vk.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message=text,
            keyboard=keyboard,
            attachment=attachment
        )
    


