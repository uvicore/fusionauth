# FusionAuth Uvicore Library


This is a basic, FusionAuth API client for uvicore projects.


## Installation

This is a Uvicore library and requires the Uvicore framework.

Install into your own uvicore app or library with
```bash
pip install uvicore-fusionauth
# or via poetry, pipenv etc...
```

**Registration**
Add this package as a dependency of your own package

Edit your `config/package.py` and add this to the `dependencies` dictionary
```python
'mreschke.fusionauth': {
    'provider': 'mreschke.fusionauth.services.fusionauth.Fusionauth
}
```

**Configuration**
If you have only one FusionAuth tenant.

Simply add these environment variables to your `.env`
```bash
# FusionAuth Client
FUSIONAUTH_URL="https://auth.youridp.com"
FUSIONAUTH_DEFAULT_TENANT='default'
FUSIONAUTH_KEY_MASTER='abc'
FUSIONAUTH_KEY_TENANT_DEFAULT="xyz"
```

If you have more than one tenant and want to be able to query all of them.

Create config override in your service provider so you can override `mreschke.fusionauth` `tenant_keys` config dictionary with a list of your own tenants.

Edit your apps `services/yourapp.py` service provider.  In the `register()` method, add this to your `self.configs([])`
```python
# Override mreschke.fusionauth
{'key': 'mreschke.fusionauth', 'module': 'you.yourapp.config.overrides.fusionauth.config'},
```

Now create that `config/overrides/fusionauth.py` file and override only the `tenant_keys` dictionary.
```python
from uvicore.configuration import env
from uvicore.typing import OrderedDict

# Override to mreschke.fusionauth package config
# So we can define our own tenants and keys

config = {

    # FusionAuth tenant API keys
    # If a tenant is not defined here or the key is empty, tenant access is denied
    'tenant_keys': {
        'sun': env('FUSIONAUTH_KEY_TENANT_SUN', None),
        'tge': env('FUSIONAUTH_KEY_TENANT_TGE', None),
        'tgb': env('FUSIONAUTH_KEY_TENANT_TGB', None),
    },
}
```

And override with your `.env` as needed.

Now, keep those secrets our of your code and .git by adding the actual value to your `.env` file.
```bash
# FusionAuth Client
FUSIONAUTH_URL="https://auth.youridp.com"
FUSIONAUTH_DEFAULT_TENANT='default'
FUSIONAUTH_KEY_MASTER='abc'
FUSIONAUTH_KEY_TENANT_SUN="def"
FUSIONAUTH_KEY_TENANT_TGE="ghi"
FUSIONAUTH_KEY_TENANT_TGB="jkl"
```


**Test**
To test it's all working, run `./uvicore` from your app and you should see a new command group called `fusionauth`.  There are some `fusionauth` commands in there, they should all work against your FusionAuth server and tenants if you got the config right.

