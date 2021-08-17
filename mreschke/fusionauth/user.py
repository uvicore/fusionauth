import uvicore
from uvicore.typing import Optional
from .client import Client as fa
from .models import User as User
from uvicore.support.dumper import dump, dd


async def find(id_or_email: str, tenant: Optional[str] = None) -> User:
    tenant = await fa.verify_tenant(tenant)

    # Get by ID or email
    url = 'api/user/'
    if '@' in id_or_email: url += '?email='
    url = url + id_or_email

    async def query():
        r = await fa.get(url, tenant)
        dump(r)
        return User.mapper(r.get('user')).model()
    return await uvicore.cache.remember(tenant + '/' + url, query)


async def search(query: str, page: int = 1, limit: int = 25, tenant: Optional[str] = None):
    """Search for users with a query"""
    tenant = await fa.verify_tenant(tenant)

    # FA does not have a get all users api.  Too large.  You must search and page.
    # My page starts on 1, but FA starts on 0
    if page == 0: page = 1
    page = (page - 1) * limit

    url = 'api/user/search?queryString={}&numberOfResults={}&startRow={}'.format(query, limit, page)
    async def query():
        r = await fa.get(url, tenant)
        return User.mapper(r.get('users')).model()
    return await uvicore.cache.remember(tenant + '/' + url, query)
