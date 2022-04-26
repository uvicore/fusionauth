import uvicore
from mreschke.fusionauth.client import Client as fa
from uvicore.support.dumper import dump, dd
from uvicore.typing import Dict, List, Optional
from uvicore.exceptions import SmartException

URL = 'api/api-key'

async def find(id: str) -> Dict:
    """Get one api key by ID"""
    default_tenant = await fa.verify_tenant()
    url = URL + '/' + id
    try:
        async def query():
            response = await fa.get(url, default_tenant, master_key = True)
            return Dict(response['apiKey'])
        return await uvicore.cache.remember(default_tenant + '/' + url, query)
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)

async def upsert(params: Dict) -> None:
    default_tenant = await fa.verify_tenant()
    params = Dict(params)

    # Validate some params
    if not params.id:
        raise SmartException("Parameter 'id' not found")
    if not params.key:
        raise SmartException("Parameter 'key' not found")

    # Url
    url = URL + '/' + str(params.id)

    # Check if api key exists
    exists = False
    try:
        existing = await find(params.id)
        exists = True
    except SmartException as e:
        pass

    try:
        if exists:
            # Update existing api key (full POST)
            await fa.put(url, default_tenant, master_key=True, json={'apiKey': params})
        else:
            # Insert new api key
            await fa.post(url, default_tenant, json={'apiKey': params})
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)
