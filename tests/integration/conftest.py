from datetime import datetime
import pytest

from kore import config_factory, container_factory


@pytest.fixture(scope='session')
def beaker_config():
    return {
        'cache.data_dir':'./cache',
        'cache.type':'dbm',
        'cache.expire': 2,
        'cache.regions': 'short_term, long_term',
        'cache.short_term.expire': '2',
    }


@pytest.fixture(scope='session')
def config(beaker_config):
    return config_factory.create('dict', **{'beaker': beaker_config})


@pytest.fixture
def container(config):
    initial = {
        'config': config,
    }
    return container_factory.create(**initial)


@pytest.fixture
def cache_manager(container):
    return container('kore.components.beaker.cache.manager')


@pytest.fixture
def cached_func(cache_manager):
    @cache_manager.cache('loader')
    def load(person):
        now = datetime.now()
        return "Hi there %s, its currently %s" % (person, now)
    return load


@pytest.fixture
def region_cached_func(cache_manager):
    @cache_manager.region('short_term', 'region_loader')
    def load(person):
        now = datetime.now()
        return "Hi there %s, its currently %s" % (person, now)
    return load
