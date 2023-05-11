#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker"""
import requests
from redis import Redis
from typing import Callable
from functools import wraps

r_count = Redis()


def count_req(method: Callable) -> Callable:
    """decorator counter"""
    @wraps(method)
    def wrapper(url):
        """count"""
        r_count.incr(f"count:{url}")
        c_html = r_count.get(f"exp:{url}")
        if c_html:
            return c_html.decode('utf-8')

        url_html = method(url)
        r_count.setex(f"exp:{url}", 10, url_html)
        return url_html

    return wrapper


@count_req
def get_page(url: str) -> str:
    """exipring cache"""
    response = requests.get(url)
    return response.text
