import random
import string

from django_utils_morriswa.view_utils import WView


def id_generator(size=4, chars=string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


class AnyView(WView):
    authentication_classes = []
    permission_classes = []
