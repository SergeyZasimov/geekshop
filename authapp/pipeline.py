import requests
import datetime
from django.utils.timezone import now
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile

from social_core.backends.github import GithubOAuth2
from django.conf import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':

        api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,city,photo_200_orig,country,domain&access_token={response['access_token']}&v=5.92"

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]

        if data['sex']:
            if data['sex'] == 1:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE
            elif data['sex'] == 2:
                user.shopuserprofile.gender = ShopUserProfile.MALE

        if data['about']:
            user.shopuserprofile.about_me = data['about']

        if data['bdate']:
            bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            user.age = now().date().year - bdate.year
            if user.age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        if data['photo_200_orig']:
            img = requests.get(data['photo_200_orig'])
            img_file = open(f"media/users_avatar/{data['id']}.jpg", "wb")
            img_file.write(img.content)
            img_file.close()

            user.avatar = f"users_avatar/{data['id']}.jpg"

        if data['city']:
            user.shopuserprofile.city = data['city']['title']

        if data['country']:
            user.shopuserprofile.country = data['country']['title']

        user.save()

    else:
        return



