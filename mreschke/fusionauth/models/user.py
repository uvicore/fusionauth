from __future__ import annotations

import uvicore
from typing import Optional, List
from uvicore.support.dumper import dd, dump
from uvicore.orm import Model, ModelMetaclass, BelongsTo, Field
#from sunfinity.iam.database.tables import tenants as table

#from .tenant import Tenant


@uvicore.model()
class User(Model['User'], metaclass=ModelMetaclass):
    """Iam User Model"""

    # Database table definition
    #__tableclass__ = table.Tenants

    # API Model instance variables
    __api_key__: str
    __url__: str

    id: str = Field('id',
        primary=True,
        description='User ID',
        #read_only=True,
    )

    email: str = Field('email',
        description='Email',
        #required=True,
        #read_only=True,
    )

    first_name: str = Field('firstName',
        description='Users First Name',
    )

    last_name: str = Field('lastName',
        description='Users Last Name',
    )

    tenant_id: str = Field('tenantId',
        description='Users Tenant ID',
    )

    active: bool = Field('active',
        description='User is Active',
    )

    roles: List = Field(None,
        description='Users Roles'
    )

    # tenant: Optional[Tenant] = Field(
    #     description='Users Tenant',
    #     relation=BelongsTo('sunfinity.iam.models.Tenant')
    # )

    @classmethod
    async def get(entity, queries):
        dump(queries)
        return {'hi': entity.__api_key__}
        dump('user model get here!')
