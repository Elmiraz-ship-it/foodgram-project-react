from typing import List, Optional

from users.models import CustomUser, Follow


def new_follow(user: CustomUser, author: CustomUser) -> Optional[Follow]:
    try:
        new = Follow(user=user, author=author)
        new.save()
        return new
    except Exception as e:
        print('follow error:', str(e))
        return None


def get_subscribes_on(user: CustomUser) -> List[CustomUser]:
    subs = [f.author for f in user.follower.all().select_related('author')]
    return subs


def unsubscribe_user_from(user: CustomUser, author: CustomUser) -> bool:
    try:
        Follow.objects.get(user=user, author=author).delete()
        return True
    except Follow.DoesNotExist:
        return False
