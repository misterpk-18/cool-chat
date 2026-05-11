from datetime import datetime
from flask import request


def log_request():

    print("\n========== REQUEST ==========")

    print(f"Time : {datetime.now()}")

    print(f"Method : {request.method}")

    print(f"URL : {request.url}")

    print(f"IP : {request.remote_addr}")

    print("=============================\n")