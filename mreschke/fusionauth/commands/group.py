import uvicore
from mreschke.fusionauth.repository import group
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException
from mreschke.fusionauth.support.json import to
from uvicore.console import command, argument, option


@command()
@argument('id_or_name')
@option('--tenant', help='FusionAuth tenant')
@option('--json', is_flag=True, help='Output results as JSON')
async def get(id_or_name: str, tenant: str, json: bool):
    """Get one group by ID or name"""
    # ex: ./uvicore fusionauth group get 8b83d29d-36bb-4137-aeb8-8e771fda3443
    # ex: ./uvicore fusionauth group get Administrator
    try:
        dump(to(json, await group.find(id_or_name, tenant=tenant)))
    except SmartException as e:
        #print(e.detail)
        print(e.message)
        exit(e.status_code)


@command()
@option('--tenant', help='FusionAuth tenant')
@option('--json', is_flag=True, help='Output results as JSON')
async def list(tenant: str, json: bool):
    """List all group"""
    # ex: ./uvicore fusionauth group list
    try:
        dump(to(json, await group.list(tenant=tenant)))
    except SmartException as e:
        #print(e.detail)
        print(e.message)
        exit(e.status_code)



