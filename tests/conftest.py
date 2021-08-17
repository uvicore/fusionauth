import pytest
import asyncio
import uvicore
from uvicore.support.dumper import dump, dd


@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def fusionauth(event_loop):

    # Setup Tests
    ############################################################################
    # Bootstrap uvicore application
    from mreschke.fusionauth.services import bootstrap
    bootstrap.application(is_console=False)

    # Drop/Create and Seed SQLite In-Memory Database
    # from mreschke.fusionauth.database.seeders import seed
    # engine = uvicore.db.engine()
    # metadata = uvicore.db.metadata()
    # metadata.drop_all(engine)
    # metadata.create_all(engine)
    # await seed()


    # Run ALL Tests
    ############################################################################

    yield ''

    # Tear down tests
    ############################################################################
    #metadata.drop_all(engine)

