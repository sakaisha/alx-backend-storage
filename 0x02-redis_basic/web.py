#!/usr/bin/env python3
"""
Implementing an expriting web cache and tracker
"""
import requests
import redis
import time


redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_page(url: str) -> str:
    """
    Fetches HTML content from URL
    """
    cached_html = redis_client.get(url)

    if cached_html:
        print(f"{Returning cached content for {url}")
        return cached_html.decode('utf-8')

    response = requests.get(url)
    html_content = response.text

    redis_client.setex(url, 10, html_content)

    count_key = f"count:{url}"
    redis_client.incr(count_key)

    print(f"Feteched new content for {url}")

    return html_content
