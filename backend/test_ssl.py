import requests
import certifi
import os
import requests
r = requests.get("https://www.youtube.com", verify=False, timeout=10)
print("SUCCESS:", r.status_code)


# print("certifi CA:", certifi.where())
# os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
# url = "https://www.youtube.com"

# try:
#     r = requests.get(url, timeout=10)
#     print("SUCCESS:", r.status_code)
# except Exception as e:
#     print("ERROR:", type(e).__name__, e)
