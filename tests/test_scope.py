from webscanner.core.scope import normalize_target, same_origin

def test_normalize():
    assert normalize_target("example.com") == "https://example.com"

def test_same_origin():
    assert same_origin("https://a.test/x", "https://a.test/y")
    assert not same_origin("https://a.test/x", "https://b.test/y")