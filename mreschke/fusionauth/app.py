import uvicore
from .client import Client as fa
from uvicore.typing import Optional, List

from uvicore.support.dumper import dump, dd
from .models import App


async def find(id_or_name: str, tenant: Optional[str] = None) -> App:
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
    async def query():
        r = await fa.get(url, tenant)
        return App.mapper(r.get('application')).model()
    return await uvicore.cache.remember(tenant + '/' + url, query)


async def list(tenant: Optional[str] = None) -> List[App]:
    """Get all applications"""
    tenant = await fa.verify_tenant(tenant)

    url = 'api/application'
    async def query():
        r = await fa.get(url, tenant)
        return App.mapper(r.get('applications')).model()
    return await uvicore.cache.remember(tenant + '/' + url, query)
