import uvicore
from uvicore.configuration import env
from uvicore.support.dumper import dump, dd
from uvicore.typing import Dict
from uvicore.exceptions import SmartException


@uvicore.service('mreschke.fusionauth.client.Client',
    aliases=['fusionauth'],
    singleton=True
)
class Client:
    """Generic Async AIOHTTP Rest client for FusionAuth"""

    @property
    def config(self):
        return uvicore.config.mreschke.fusionauth

    @property
    def allowed_tenants(self):
        return [k for (k,v) in self.config.tenant_keys.items() if v]

    async def verify_tenant(self, tenant: str = None):
        if tenant is None: tenant = self.config.default_tenant or 'default'
        if tenant.lower() not in self.allowed_tenants:
            await self.not_found('Invalid tenant.  Must be one of {}'.format(str(self.allowed_tenants)))
        return tenant.lower()

    async def api_key(self, tenant: str, master_key: bool = False) -> str:
        if master_key:
            key = self.config.master_key
        else:
            key: str = self.config.tenant_keys[tenant]
        if key: return key
        await self.not_found('API key not found in config for tenant {}'.format(tenant))

    async def url(self, path: str) -> str:
        auth_url = self.config.url
        if auth_url[-1] == '/': auth_url = auth_url[0:-1]  # Remove trailing / from base
        if path[0] == '/': path = path[1:]  # Remove leading / from path
        if auth_url: return auth_url + '/' + path
        await self.not_found('FusionAuth URL not found in config')

    async def get(self, path: str, tenant: str = None, master_key: bool = False):
        # Get aiohttp client session from IoC singleton
        http = uvicore.ioc.make('aiohttp')

        # Get proper API key
        key = await self.api_key(tenant, master_key)

        # Get full URL
        url = await self.url(path)

        # Async aiohttp GET
        async with http.get(url, headers={'Authorization': key}) as r:
            #dump(r)
            if r.status == 200:
                return await r.json()
            try:
                #dump('x')
                #detail='x'
                detail = await r.json()
            except:
                detail = await r.text()
            await self.exception(detail or 'Not Found', status_code=r.status)

    async def post(self, path: str, tenant: str = None, master_key: bool = False, json: Dict = None):
        # Get aiohttp client session from IoC singleton
        http = uvicore.ioc.make('aiohttp')

        # Get proper API key
        key = await self.api_key(tenant, master_key)

        # Get full URL
        url = await self.url(path)

        async with http.post(url, json=json, headers={'Authorization': key}) as r:
            #dump(r)
            if r.status == 200:
                return await r.json()
            try:
                #dump('x')
                #detail='x'
                detail = await r.json()
            except:
                detail = await r.text()
            await self.exception(detail or 'Not Found', status_code=r.status)

    async def put(self, path: str, tenant: str = None, master_key: bool = False, json: Dict = None):
        # Get aiohttp client session from IoC singleton
        http = uvicore.ioc.make('aiohttp')

        # Get proper API key
        key = await self.api_key(tenant, master_key)

        # Get full URL
        url = await self.url(path)

        async with http.put(url, json=json, headers={'Authorization': key}) as r:
            #dump(r)
            if r.status == 200:
                return await r.json()
            try:
                #dump('x')
                #detail='x'
                detail = await r.json()
            except:
                detail = await r.text()
            await self.exception(detail or 'Not Found', status_code=r.status)

    async def patch(self, path: str, tenant: str = None, master_key: bool = False, json: Dict = None):
        # Get aiohttp client session from IoC singleton
        http = uvicore.ioc.make('aiohttp')

        # Get proper API key
        key = await self.api_key(tenant, master_key)

        # Get full URL
        url = await self.url(path)

        async with http.patch(url, json=json, headers={'Authorization': key}) as r:
            #dump(r)
            if r.status == 200:
                return await r.json()
            try:
                #dump('x')
                #detail='x'
                detail = await r.json()
            except:
                detail = await r.text()
            await self.exception(detail or 'Not Found', status_code=r.status)

    async def not_found(self, message: str):
        if uvicore.app.is_http:
            from uvicore.http.exceptions import NotFound
            raise NotFound(message)
        else:
            await uvicore.ioc.make('aiohttp').close()
            raise Exception(message)

    async def exception(self, message: str, *, status_code=503):
        raise SmartException(message, status_code)
        # if uvicore.app.is_http:
        #     from uvicore.http.exceptions import HTTPException
        #     raise HTTPException(detail=message, status_code=status_code)
        # else:
        #     dump('xxxxx')
        #     await uvicore.ioc.make('aiohttp').close()
        #     raise Exception(message + ' - Status Code ' + str(status_code))
