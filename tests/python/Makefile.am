check_SCRIPTS = test_inetdomain.py test_zone.py test_matcher.py test_dispatch.py test_nat.py test_log.py test_session.py test_keybridge.py test_chainer.py

AM_TESTS_ENVIRONMENT = G_DEBUG='fatal_warnings gc-friendly'; G_SLICE='always-malloc' ; export G_DEBUG; export G_SLICE; PYTHONPATH=$(top_srcdir)/pylib:$(top_builddir)/pylib/Zorp:$(top_srcdir)/pylib/kzorp:$(PYTHONPATH)

TEST_EXTENSIONS = .py
PY_LOG_COMPILER = $(top_builddir)/zorp/zorp
AM_PY_LOG_FLAGS = -F --no-syslog --no-caps -p

TESTS = $(check_SCRIPTS)
EXTRA_DIST = $(check_SCRIPTS)
