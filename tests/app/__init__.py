# flake8: noqa: F401
import threading
import contextlib
import time

from litestar import Litestar, status_codes
from litestar.config.cors import CORSConfig

import uvicorn

from .app import (
    index,
    webhook,
    test_raw_payload,
    set_signing_secret,
    get_signing_secret,
    get_webhook_payload,
    internal_server_error_handler,
)

app = Litestar(
    route_handlers=[
        index,
        webhook,
        set_signing_secret,
        test_raw_payload,
        get_signing_secret,
        get_webhook_payload,
    ],
    cors_config=CORSConfig(allow_origins=["*"]),
    exception_handlers={
        status_codes.HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
)


class UvicornServer(uvicorn.Server):
    def install_singal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        """Run the server in a separate thread.

        Parameters
        ----------
        None

        Yields
        ------
        None

        """
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()
