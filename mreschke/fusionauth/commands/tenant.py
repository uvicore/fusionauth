import uvicore
from mreschke.fusionauth.repository import tenant
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException
from mreschke.fusionauth.support.json import to
from uvicore.console import command, argument, option


@command()
@argument('id_or_name')
@option('--json', is_flag=True, help='Output results as JSON')
async def get(id_or_name: str, json: bool):
    """Get one tenant by ID or name"""
    # ex: ./uvicore fusionauth tenant get 8b83d29d-36bb-4137-aeb8-8e771fda3443
    # ex: ./uvicore fusionauth tenant get Default
    try:
        dump(to(json, await tenant.find(id_or_name)))
    except SmartException as e:
        #print(e.detail)
        print(e.message)
        exit(e.status_code)


@command()
@option('--json', is_flag=True, help='Output results as JSON')
async def list(json: bool):
    """List all tenants"""
    # ex: ./uvicore fusionauth tenant list
    try:
        dump(to(json, await tenant.list()))
    except SmartException as e:
        #print(e.detail)
        print(e.message)
        exit(e.status_code)


