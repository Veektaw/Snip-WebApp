import random
import string
from app.snipe.models import Url
from flask import request 
import re
import qrcode
import io
import secrets
from datetime import datetime  
from ..snipe.utils import db
from ..snipe.models import User

def check_valid_url(url):
    
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # scheme
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return (regex.match(url))


class URLCreator:

    @classmethod
    def short_url(cls, url):
        characters_combination = string.ascii_letters + string.digits
        random_string_combination = ''.join(random.choices(characters_combination, k=5))
        short_url = f"http://{request.host}/{random_string_combination}"
        does_url_exist = Url.check_url(short_url)

        if does_url_exist:
            return cls.short_url(url)

        return short_url
    
    
    @classmethod
    def generate_custom_url_entry(cls, custom_url_entry):
        existing_url = Url.query.filter_by(custom_url=custom_url_entry).first()
        if existing_url:
       
            return cls.generate_custom_url_entry(custom_url_entry)
        else:
        
         return custom_url_entry

    
    
    @classmethod
    def custom_url(cls, url, custom_url_entry):
        custom_url = f"http://{request.host}/{cls.generate_custom_url_entry(custom_url_entry)}"
        does_url_exist = Url.check_url(custom_url)

        if does_url_exist:
            return cls.custom_url(url, custom_url_entry)

        return custom_url





    

    @classmethod
    def is_valid_url(cls, url): 
        """"Check if a url is valid or not"""
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # scheme
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url 

    @classmethod
    def extract_url_data(cls, url): 
        from bs4 import BeautifulSoup
        import requests
        
        response = requests.get(url)

        
        soup = BeautifulSoup(response.content, 'html.parser')

        
        try:
            title = soup.title.string
        except:
            title = ''

        
        return title





from urllib.parse import urlparse

def url_validate(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
    
def generate_qr_code(url):
    img = qrcode.make(url)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
