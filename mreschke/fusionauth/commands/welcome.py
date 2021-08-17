import uvicore
from time import sleep
from uvicore.console import command
from uvicore.support.dumper import dump, dd


@command()
async def cli():
    """Welcome to Uvicore"""

    from mreschke.fusionauth.client import Client as fa
    #client = uvicore.ioc.make('fusionauth')

    #await fa.verify_tenant('sun')

    #dump(await fa.get('/api/user/?email=it@sunfinity.com', 'sun'))

    #dump(await fa.get('/api/tenant', master_key=True))

    dump(await fa.get('/api/application', master_key=True))



    # from uvicore import cache
    # from time import time


    # async def stuff():
    #     dump('CALLBACK')
    #     return 'stuff here'


    # await cache.put('name', 'matthew', seconds=0)

    # for i in range(1, 20):
    #     dump(await cache.remember('stuff', stuff, seconds=5))
    #     dump(await cache.get('name'))
    #     dump(cache.__dict__)
    #     dump(int(time()))
    #     sleep(1)

