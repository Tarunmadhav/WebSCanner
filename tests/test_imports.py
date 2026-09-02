def test_imports():
    import webscanner
    import webscanner.cli
    import webscanner.core.orchestrator
    import webscanner.checks.xss
    import webscanner.checks.injection
    import webscanner.zap.client
    assert webscanner.__version__