# List of blacklisted URLs to decrease complexity of link traversal
# NOTE: The subroutes for these URLs are not blacklisted (e.g: https://cloud.google.docs/vertex-ai will not be blacklisted)

BLACKLIST_URLS = [
    "https://cloud.google.com/",
    "https://cloud.google.com/docs"
]

# Alternatively only allow certain URLs and their sub-routes
WHITELIST_URLS = [
    "https://cloud.google.com/vertex-ai/docs/generative-ai/",
    "https://cloud.google.com/vertex-ai/docs/quotas"
]

# The URL to start the scraping process from
ROOT_URL = "https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview"