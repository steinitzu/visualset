from gevent import monkey

monkey.patch_all(thread=False)

from . import dependencies
