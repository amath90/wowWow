import logging
import traceback
from functools import wraps


logger = logging.getLogger(__name__)


def clean_on_failure(clean_handler):
    """
    In case of Exception or KeyboardInterrupt will call clean_handler
    """

    def decorator(decorated_function):

        @wraps(decorated_function)
        def wrapper(*args, **kwargs):
            try:
                return decorated_function(*args, **kwargs)
            except (Exception, KeyboardInterrupt):
                logger.error('Caught exception: %s', traceback.format_exc())
                clean_handler(args[0])

        return wrapper

    return decorator
