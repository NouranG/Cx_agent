SOURCES = [
    {
        "name": "att",
        "base_url": "https://www.att.com/support/",
        "allowed_prefixes": (
            "/support/article/",
            "/support/pages/"
        ),
        "max_depth": 2,
        "max_pages": 100
    },
    {
        "name": "cloudflare",
        "base_url": "https://developers.cloudflare.com/",
        "allowed_prefixes": (
            "/support/",
            "/fundamentals/",
            "/learning-paths/"
        ),
        "max_depth": 3,
        "max_pages": 300
    }
]