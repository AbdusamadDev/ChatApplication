# import time
# import requests
# import json


# host = "androidserver.pythonanywhere.com"

# creation = requests.post(
#     f"http://{host}/api/mud/",
#     json={
#         "longitude": "69.2401",
#         "latitude": "41.2995",
#     },
# )
# print("Client created: ", creation.json())
# print(creation.status_code)
# # Tashkent
# while True:
#     try:
#         print(
#             requests.get(
#                 f"http://{host}/api/mud/",
#                 headers={
#                     "longitude": "69.2401",
#                     "latitude": "41.2995",
#                 },
#             ).json(),
#         )
#         time.sleep(3)
#     except KeyboardInterrupt:
#         requests.delete(
#             f"http://{host}/api/mud/" + str(creation.json().get("client_pk"))
#         )
#         break

from turtle import *
import colorsys

bgcolor("black")
tracer(5)
h = 0
for i in range(1000):
    c = colorsys.hsv_to_rgb(h, 1, 1)
    color(c)
    begin_fill()
    forward(i)
    left(21)
    backward(i * 0.5)
    circle(i * 3)
    end_fill()
    h += 0.008

done()
