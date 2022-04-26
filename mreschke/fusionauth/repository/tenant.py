import uvicore
from mreschke.fusionauth.client import Client as fa
from uvicore.support.dumper import dump, dd
from uvicore.typing import Dict, List, Optional
from uvicore.exceptions import SmartException

URL = 'api/tenant'

async def find(id_or_name: str) -> Dict:
    """Get one tenant by ID or name"""
    default_tenant = await fa.verify_tenant()

    # Get application by name
    # FusionAuth does not have an endpoint to get by name, so we'll get all and filter
    is_guid = len(id_or_name) == 36 and id_or_name.count('-') == 4
    if not is_guid:
        tenants = await list()
        for tenant in tenants:
            if tenant.name == id_or_name:
                return tenant
        return None

    url = URL + '/' + id_or_name
    try:
        async def query():
            response = await fa.get(url, default_tenant)
            return Dict(response['tenant'])
        return await uvicore.cache.remember(default_tenant + '/' + url, query)
    except SmartException as e:
        dump(e)
        raise SmartException(e.detail, message='Cannot query ' + url)


async def list() -> List[Dict]:
    """Get all applications"""
    tenant = await fa.verify_tenant()
    url = URL
    response = ''
    try:
        async def query():
            response = await fa.get(url, tenant)
            if not response: response['tenants'] = []
            return [Dict(x) for x in response.get('tenants')]
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)


async def upsert(params: Dict) -> None:
    default_tenant = await fa.verify_tenant()
    params = Dict(params)

    # Validate some params
    if not params.id:
        raise SmartException("Parameter 'id' not found")
    if not params.name:
        raise SmartException("Parameter 'name' not found")

    # Url
    url = URL + '/' + str(params.id)

    # Check if tenant exists and also get the Default tenant as a template
    exists = False
    template = {}
    tenants = await list()
    for tenant in tenants:
        if tenant.name.lower() == params.name.lower():
            exists = True
        if tenant.name.lower() == 'default':
            template = tenant.clone()

    if not template:
        raise SmartException("Default tenant not found, not sure what to use for a template.")

    try:
        if exists:
            # Update existing tenant (partial with a PATCH)
            await fa.patch(url, default_tenant, json={'tenant': params})
        else:
            # Insert new tenant using the Default as a template, merged with our params
            await fa.post(url, default_tenant, json={'tenant': template.merge(params)})
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)
