import uvicore
from mreschke.fusionauth.client import Client as fa
from uvicore.support.dumper import dump, dd
from uvicore.typing import Dict, List, Optional
from uvicore.exceptions import SmartException


async def find(id_or_name: str, tenant: Optional[str] = None) -> Dict:
    """Get one group by ID or name"""
    tenant = await fa.verify_tenant(tenant)

    # Get group by name
    # FusionAuth does not have an endpoint to get by name, so we'll get all and filter
    is_guid = len(id_or_name) == 36 and id_or_name.count('-') == 4
    if not is_guid:
        groups = await list(tenant)
        for group in groups:
            if group.name == id_or_name:
                return group
        return None

    url = 'api/group/' + id_or_name
    try:
        async def query():
            response = await fa.get(url, tenant)
            return Dict(response['group'])
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)


async def list(tenant: Optional[str] = None) -> List[Dict]:
    """Get all groups"""
    tenant = await fa.verify_tenant(tenant)

    url = 'api/group'
    try:
        async def query():
            response = await fa.get(url, tenant)
            return [Dict(x) for x in response.get('groups')]
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)
