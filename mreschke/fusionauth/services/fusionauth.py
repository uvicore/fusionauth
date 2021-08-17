import uvicore
from uvicore.console.provider import Cli
from uvicore.package import ServiceProvider
from uvicore.support.dumper import dump, dd


@uvicore.provider()
class Fusionauth(ServiceProvider, Cli):

    def register(self) -> None:
        """Register package into the uvicore framework.
        All packages are registered before the framework boots.  This is where
        you define your packages configs, IoC bindings and early event listeners.
        Configs are deep merged only after all packages are registered.  No real
        work should be performed here as it is very early in the bootstraping
        process and we have no clear view of the full configuration system."""

        # Register configs
        # If config key already exists items will be deep merged allowing
        # you to override granular aspects of other package configs
        self.configs([
            # Here self.name is your packages name (ie: mreschke.fusionauth).
            {'key': self.name, 'module': 'mreschke.fusionauth.config.package.config'},

            # Example of splitting out the app config into multiple files per section
            #{'key': self.name, 'module': 'mreschke.fusionauth.config.database.config'},

            # Example of how to override another packages config with your own.
            #{'key': 'uvicore.auth', 'module': 'mreschke.fusionauth.config.overrides.auth.config'},
        ])

        # Force quick bind of provider by importing it high up
        from mreschke.fusionauth.client import Client

    def boot(self) -> None:
        """Bootstrap package into the uvicore framework.
        Boot takes place after ALL packages are registered.  This means all package
        configs are deep merged to provide a complete and accurate view of all
        configuration. This is where you register, connections, models,
        views, assets, routes, commands...  If you need to perform work after ALL
        packages have booted, use the event system and listen to the booted event:
        self.events.listen('uvicore.foundation.events.app.Booted, self.booted')"""

        # Define Service Provider Registrations
        self.registers(self.package.config.registers)

        # Define CLI commands to be added to the ./uvicore command line interface
        self.define_commands()

    def define_commands(self) -> None:
        """Define CLI commands to be added to the ./uvicore command line interface"""

        # Fusionauth
        self.commands(
            group='fusionauth',
            help='Fusionauth Commands',
            commands={},
        )

        # Apps command
        self.commands(
            group='fusionauth:apps',
            help='FusionAuth Applications',
            commands={
                'list': 'mreschke.fusionauth.commands.apps.list',
                'get': 'mreschke.fusionauth.commands.apps.get',
            },
        )
