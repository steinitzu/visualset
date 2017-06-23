from gevent import monkey

monkey.patch_all(thread=True)

from . import dependencies
