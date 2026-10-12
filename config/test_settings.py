"""Private, synthetic settings and network denial for local automated tests."""

from __future__ import annotations

import os
import secrets
import tempfile
from pathlib import Path

from tests.support import install_network_denial

_PRIVATE_ROOT = tempfile.TemporaryDirectory(prefix="career-helper-django-tests-")
_PRIVATE_PATH = Path(_PRIVATE_ROOT.name)
_PRIVATE_PATH.chmod(0o700)

os.environ["CAREER_HELPER_ENV"] = "test"
os.environ["CAREER_HELPER_DEBUG"] = "false"
os.environ["CAREER_HELPER_SECRET_KEY"] = secrets.token_urlsafe(48)
os.environ["CAREER_HELPER_ALLOWED_HOSTS"] = "localhost,127.0.0.1,::1"
os.environ["CAREER_HELPER_DATA_ROOT"] = str(_PRIVATE_PATH / "data")
os.environ["CAREER_HELPER_TEST_DATA_ROOT"] = str(_PRIVATE_PATH / "test-data")
os.environ["CAREER_HELPER_FIXTURE_MODE"] = "true"
os.environ["CAREER_HELPER_EXTERNAL_NETWORK_ENABLED"] = "false"

install_network_denial()

from .settings import *  # noqa: F403, E402
