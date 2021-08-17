import json as JSON
import uvicore
from uvicore.typing import List
from mreschke.fusionauth import app
from uvicore.support.dumper import dump, dd
from uvicore.console import command, argument, option
from uvicore.exceptions import SmartException
from mreschke.fusionauth.support.json import to

@command()
@option('--json', is_flag=True, help='Output results as JSON')
async def list(json: bool):
    """List all applications"""
    # ex: ./uvicore fusionauth apps list
    try:
        dump(to(json, await app.list()))
    except SmartException as e:
        exit(e.detail)


@command()
@argument('id')
@option('--json', is_flag=True, help='Output results as JSON')
async def get(id: str, json: bool):
    """Get one application by name or ID"""
    # ex: ./uvicore fusionauth apps get 8b83d29d-36bb-4137-aeb8-8e771fda3443
    try:
        dump(to(json, await app.find(id)))
    except SmartException as e:
        exit(e.detail)
