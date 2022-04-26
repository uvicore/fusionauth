from uvicore.configuration import env
from uvicore.typing import OrderedDict

# This is the main fusionauth config.  All items here can be overridden
# when used inside other applications.  Accessible at config('mreschke.fusionauth')

config = {

    # FusionAuth base URL
    'url': env('FUSIONAUTH_URL', 'https://auth.example.com'),

    # Default tenant if none defined
    'default_tenant': env('FUSIONAUTH_DEFAULT_TENANT', 'default'),

    # FusionAuth master API key
    # Optional if you want to access multi-tenant endpoints like /tenants
    'master_key': env('FUSIONAUTH_KEY_MASTER', None),

    # FusionAuth tenants (short names, does not have to match actual FusionAuth tenant names)
    # See at bottom, there is a config override to add tenant_keys which is
    # a dynamic Dict based on all tenants ENV vars
    'tenants': env.list('FUSIONAUTH_TENANTS', ['default']),


    # --------------------------------------------------------------------------
    # Registration Control
    # --------------------------------------------------------------------------
    # This lets you control the service provider registrations.  If this app
    # is used as a package inside another app you might not want some things
    # registered in that context.  Use config overrides in your app to change
    # registrations
    # 'registers': {
    #     'web_routes': False,
    #     'api_routes': False,
    #     'middleware': False,
    #     'views': False,
    #     'assets': False,
    #     'commands': False,
    #     'models': False,
    #     'tables': False,
    #     'seeders': False,
    # },


    # --------------------------------------------------------------------------
    # Package Dependencies (Service Providers)
    #
    # Define all the packages that this package depends on.  At a minimum, only
    # the uvicore.foundation package is required.  The foundation is very
    # minimal and only depends on configuratino, logging and console itself.
    # You must add other core services built into uvicore only if your package
    # requires them.  Services like uvicore.database, uvicore.orm, uvicore.auth
    # uvicore.http, etc...
    # --------------------------------------------------------------------------
    'dependencies': OrderedDict({
        'uvicore.foundation': {
            'provider': 'uvicore.foundation.services.Foundation',
        },
        'uvicore.http_client': {
            'provider': 'uvicore.http_client.services.HttpClient',
        },
    }),

}


# Override the config with dynamic ENV variables
config['tenant_keys'] = {}
for tenant in config['tenants']:
    config['tenant_keys'][tenant] = env('FUSIONAUTH_KEY_TENANT_' + tenant.upper(), None)

