def makeTestApp(user = "admin"):
    from ddbmock import main
    app = main({})
    from webtest import TestApp
    return TestApp(app, extra_environ = {"HTTP_AUTHORIZATION": "AWS4-HMAC-SHA256 Credential=%s" % user})
