import os
import json
import shopify
import aiohttp
import binascii

import xml.etree.ElementTree as ET

from app.settings.credentials import Connector
from app.libs.helper import get_basic_auth_header,  generate_correlation_id, xml_to_dict, xml_to_json

class Overstocks:
    async def GET(params="", headers={}, body={}):
        endpoint = Connector.endpoint

        headers["client_id"] = Connector.clientId
        headers["client_secret"] = Connector.clientSecret

        url = endpoint+params

        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def POST(params="", headers={}, body={}):
        endpoint = Connector.endpoint

        headers["client_id"] = Connector.clientId
        headers["client_secret"] = Connector.clientSecret

        url = endpoint+params

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def PUT(params="", headers={}, body={}):
        endpoint = Connector.endpoint

        headers["client_id"] = Connector.clientId
        headers["client_secret"] = Connector.clientSecret

        url = endpoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def PATCH(params="", headers={}, body={}):
        endpoint = Connector.endpoint

        headers["client_id"] = Connector.clientId
        headers["client_secret"] = Connector.clientSecret

        url = endpoint+params

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def DELETE(params="", headers={}, body={}):
        endpoint = Connector.endpoint

        headers["client_id"] = Connector.clientId
        headers["client_secret"] = Connector.clientSecret

        url = endpoint+params

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response