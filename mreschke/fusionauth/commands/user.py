import uvicore
from mreschke.fusionauth import user
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException
from mreschke.fusionauth.support.json import to
from uvicore.console import command, argument, option


@command()
@argument('id_or_email')
@option('--tenant', help='FusionAuth tenant')
@option('--json', is_flag=True, help='Output results as JSON')
async def get(id_or_email: str, tenant: str, json: bool):
    """Get one user by ID or email"""
    # ex: ./uvicore fusionauth user get email@example.com
    try:
        dump(to(json, await user.find(id_or_email, tenant=tenant)))
    except SmartException as e:
        exit(e.detail)


@command()
@argument('query')
@option('--tenant', help='FusionAuth tenant')
@option('--json', is_flag=True, help='Output results as JSON')
async def search(query: str, tenant: str, json: bool):
    """Search for users with a query"""
    # ex: ./uvicore fusionauth user find bob
    try:
        dump(to(json, await user.search(query, tenant=tenant)))
    except SmartException as e:
        exit(e.detail)


