from uvicore.configuration import env
from uvicore.typing import OrderedDict

# Running application configuration.
# This config only applies if this package is running as the main application.
# Accessible at config('app')

config = {

    # --------------------------------------------------------------------------
    # App Information
    #
    # name: The human readable name of this package/app.  Like 'Matts Wiki'
    # main: The package name to run when this app is served/executed
    # --------------------------------------------------------------------------
    'name': env('APP_NAME', 'Fusionauth App'),
    'main': 'mreschke.fusionauth',
    'debug': env('DEBUG', False),


    # --------------------------------------------------------------------------
    # Package Dependencies (Service Providers)
    #
    # Packages add functionality to your applications.  In fact your app itself
    # is a package that can be used inside any other app.  Internally, Uvicore
    # framework itself is split into many packages (Config, Event, ORM, Database,
    # HTTP, Logging, etc...) which use services providers to inject the desired
    # functionality.  Always build your packages as if they were going to be
    # used as a library in someone elses app/package.  Uvicore is built for
    # modularity where all apps are packages and all packages are apps.
    #
    # Order matters for override/deep merge purposes.  Each package overrides
    # items of the previous, so the last package wins. Example, configs defined
    # in a provider with the same config key are deep merged, last one wins.
    # Defining your actual apps package last means it will win in all override
    # battles.
    #
    # If your packages relys on other packages on its own, don't define those
    # dependencies here.  Define your packages dependencnes in its package.py
    # config file instead.  This is a list of all root packages your app relies
    # on, not every dependency of those packages.
    #
    # If you want to override some classes inside any package, but not the
    # entire package provider itself, best to use the quick and easy 'bindings'
    # dictionary below.
    #
    # Overrides include: providers, configs, views, templates, assets and more
    # --------------------------------------------------------------------------
    'packages': OrderedDict({
        # Application Service Providers
        'mreschke.fusionauth': {
            'provider': 'mreschke.fusionauth.services.fusionauth.Fusionauth',
        },
    }),

    # --------------------------------------------------------------------------
    # Logging Configuration
    #
    # The uvicore.logger packages does NOT provide its own config because it
    # needs to load super early in the bootstrap process.  Do not attempt to
    # override the logger config in the usual way of deep merging with the same
    # config key.  This is the one and only location of logging config as it
    # only applies to the running app (deep merge of all packages not needed).
    # --------------------------------------------------------------------------
    'logger': {
        'console': {
            'enabled': env.bool('LOG_CONSOLE_ENABLED', True),
            'level': env('LOG_CONSOLE_LEVEL', 'INFO'),
            'colors': env.bool('LOG_CONSOLE_COLORS', True),
            'filters': [],
            'exclude': [
                'uvicore',
                'databases',
            ],
        },
        'file': {
            'enabled': env.bool('LOG_FILE_ENABLED', True),
            'level': env('LOG_FILE_LEVEL', 'INFO'),
            'file': env('LOG_FILE_PATH', '/tmp/mreschke.fusionauth.log'),
            'when': env('LOG_ROTATE_WHEN', 'midnight'),
            'interval': env.int('LOG_ROTATE_INTERVAL', 1),
            'backup_count': env.int('LOG_ROTATE_BACKUP_COUNT', 7),
            'filters': [],
            'exclude': [],
        }
    },

}
