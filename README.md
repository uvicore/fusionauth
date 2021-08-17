# FusionAuth Uvicore Library


This is a basic, partial FusionAuth API client for uvicore projects.

Work in progress, does not cover all FusionAuth API endpoints yet.


## Usage

**Installation**
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
        'sun': env('FUSIONAUTH_KEY_SUN', None),
        'tge': env('FUSIONAUTH_KEY_TGE', None),
        'sss': env('FUSIONAUTH_KEY_SSS', None),
    },
}
```

Now, keep those secrets our of your code and .git by adding the actual value to your `.env` file.
```bash
# FusionAuth Client
FUSIONAUTH_URL="https://auth.youridp.com"
FUSIONAUTH_KEY_MASTER="abc"
FUSIONAUTH_KEY_SUN="def"
FUSIONAUTH_KEY_TGE="ghi"
FUSIONAUTH_KEY_SSS="jkl"
```

**Test**
To test it's all working, run `./uvicore` from your app and you should see a new command group called `fusionauth`.  There are some `fusionauth` commands in there, they should all work against your FusionAuth server and tenants if you got the config right.

