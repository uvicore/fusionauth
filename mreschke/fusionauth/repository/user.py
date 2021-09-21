import uvicore
from mreschke.fusionauth.client import Client as fa
from uvicore.typing import Dict, List, Optional
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException


async def find(id_or_email: str, tenant: Optional[str] = None) -> Dict:
    """Get one user by ID or email"""
    tenant = await fa.verify_tenant(tenant)

    # Get by ID or email
    url = 'api/user/'
    if '@' in id_or_email: url += '?email='
    url = url + id_or_email

    try:
        async def query():
            response = await fa.get(url, tenant)
            return Dict(response['user'])
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)


async def search(query: str, page: int = 1, limit: int = 25, tenant: Optional[str] = None) -> List[Dict]:
    """Search for users with a query"""
    tenant = await fa.verify_tenant(tenant)

    # FA does not have a get all users api.  Too large.  You must search and page.
    # My page starts on 1, but FA starts on 0
    if page == 0: page = 1
    page = (page - 1) * limit

    url = 'api/user/search?queryString={}&numberOfResults={}&startRow={}'.format(query, limit, page)
    try:
        async def query():
            response = await fa.get(url, tenant)
            return [Dict(x) for x in response.get('users')]
        return await uvicore.cache.remember(tenant + '/' + url, query)
    except SmartException as e:
        raise SmartException(e.detail, message='Cannot query ' + url)
