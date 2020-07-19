from flask_login import current_user
from tracker.lib.http import permission


@permission
def can_list_addresses_and_transactions(user_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    if current_user.id == user_id:
        return True

    return False


@permission
def can_update_user(user_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    if current_user.id == user_id:
        return True

    return False
