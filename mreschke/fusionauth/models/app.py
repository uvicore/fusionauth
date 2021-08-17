from __future__ import annotations

import uvicore
from typing import Optional, List, Dict
from uvicore.support.dumper import dd, dump
from uvicore.orm import Model, ModelMetaclass, BelongsTo, Field


@uvicore.model()
class App(Model['App'], metaclass=ModelMetaclass):
    """Iam App Model"""

    # Database table definition
    #__tableclass__ = table.Tenants

    id: str = Field('id',
        primary=True,
        description='App ID',
        #read_only=True,
    )

    name: str = Field('name',
        description='App Name',
    )

    display_name: str = Field(None,
        evaluate=lambda row: row['data']['displayName'] if 'data' in row else row['name']
    )

    verbose_name: str = Field(None,
        evaluate=lambda row: row['data']['verboseName'] if 'data' in row else row['name']
    )

    icon: str = Field(None,
        evaluate=lambda row: row['data']['matIcon'] if 'data' in row else 'build'
    )

    url: str = Field(None,
        evaluate=lambda row: row['data']['url'] if 'data' in row else None
    )

    roles: List = Field(None,
        evaluate=lambda row: sorted([x['name'] for x in row['roles']]) if 'roles' in row else []
    )

    active: bool = Field('active')
    tenant_id: str = Field('tenantId')

