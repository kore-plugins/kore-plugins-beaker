from time import sleep


class TestCacheManager(object):

    def test_cached_functions(self, cached_func, region_cached_func):
        for func in (region_cached_func, cached_func):
            result = func('Fred')
            assert 'Fred' in result

            result2 = func('Fred')
            assert result == result2

            result3 = func('George')
            assert 'George' in result3
            result4 = func('George')
            assert result3 == result4

            sleep(2)
            result2 = func('Fred')
            assert result != result2

    def test_check_invalidate(self, cache_manager, cached_func):
        result = cached_func('Fred')
        assert 'Fred' in result

        result2 = cached_func('Fred')
        assert result == result2
        cache_manager.invalidate(cached_func, 'loader', 'Fred')

        result3 = cached_func('Fred')
        assert result3 != result2

        result2 = cached_func('Fred')
        assert result3 == result2

        # Invalidate a non-existent key
        cache_manager.invalidate(cached_func, 'loader', 'Fredd')
        assert result3 == result2

    def test_check_invalidate_region(self, cache_manager, region_cached_func):
        result = region_cached_func('Fred')
        assert 'Fred' in result

        result2 = region_cached_func('Fred')
        assert result == result2
        cache_manager.region_invalidate(
            region_cached_func, None, 'region_loader', 'Fred')

        result3 = region_cached_func('Fred')
        assert result3 != result2

        result2 = region_cached_func('Fred')
        assert result3 == result2

        # Invalidate a non-existent key
        cache_manager.region_invalidate(
            region_cached_func, None, 'region_loader', 'Fredd')
        assert result3 == result2
