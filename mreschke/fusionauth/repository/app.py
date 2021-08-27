import uvicore
from mreschke.fusionauth.client import Client as fa
from uvicore.support.dumper import dump, dd
from uvicore.typing import Dict, List, Optional
from uvicore.exceptions import SmartException


async def find(id_or_name: str, tenant: Optional[str] = None) -> Dict:
    """Get one application by ID or name"""
    tenant = await fa.verify_tenant(tenant)

    # Get application by name
    # FusionAuth does not have an endpoint to get by name, so we'll get all and filter
    is_guid = len(id_or_name) == 36 and id_or_name.count('-') == 4
    if not is_guid:
        apps = await list(tenant)
        for app in apps:
            if app.name == id_or_name:
                return app
        return None

    url = 'api/application/' + id_or_name
    try:
        async def query():
            response = await fa.get(url, tenant)
            return Dict(response['application'])
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        return None

async def list(tenant: Optional[str] = None) -> List[Dict]:
    """Get all applications"""
    tenant = await fa.verify_tenant(tenant)

    url = 'api/application'
    try:
        async def query():
            response = await fa.get(url, tenant)
            return [Dict(x) for x in response.get('applications')]
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        return None
