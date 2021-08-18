import uvicore
from mreschke.fusionauth import app
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException
from mreschke.fusionauth.support.json import to
from uvicore.console import command, argument, option


@command()
@argument('id_or_name')
@option('--tenant', help='FusionAuth tenant')
@option('--json', is_flag=True, help='Output results as JSON')
async def get(id_or_name: str, tenant: str, json: bool):
    """Get one application by ID or name"""
    # ex: ./uvicore fusionauth app get 8b83d29d-36bb-4137-aeb8-8e771fda3443
    # ex: ./uvicore fusionauth app get portal-vue-app
    try:
        dump(to(json, await app.find(id_or_name, tenant=tenant)))
    except SmartException as e:
        exit(e.detail)


@command()
@option('--tenant', help='FusionAuth tenant')
@option('--json', is_flag=True, help='Output results as JSON')
async def list(tenant: str, json: bool):
    """List all applications"""
    # ex: ./uvicore fusionauth app list
    try:
        dump(to(json, await app.list(tenant=tenant)))
    except SmartException as e:
        exit(e.detail)


