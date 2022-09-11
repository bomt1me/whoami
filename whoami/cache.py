from typing import Dict, Optional

import time


class _CacheItem:
    def __init__(self, obj: str, created_at: int) -> None:
        self.obj = obj
        self.created_at = created_at


class _Cache:
    def __init__(self) -> None:
        self._cache: Dict[str, _CacheItem] = {}
        self._ttl_s = 60 * 60

        self._public_user_headshot_key = "public.user.headshot"

    def _now(self) -> int:
        return int(time.time())

    def _expire(self) -> None:
        now = self._now()
        to_delete = []
        for k, v in self._cache.items():
            if (v.created_at + self._ttl_s) < now:
                to_delete.append(k)

        for k in to_delete:
            del self._cache[k]

    def _put(self, key: str, obj: str) -> None:
        self._expire()
        self._cache[key] = _CacheItem(str(obj), self._now())

    def _get(self, key: str) -> Optional[str]:
        self._expire()
        obj = self._cache.get(key)
        if obj:
            return obj.obj

        return None

    def put_headshot(self, headshot: str) -> Optional[str]:
        self._put(self._public_user_headshot_key, headshot)

    def get_headshot(self) -> Optional[str]:
        return self._get(self._public_user_headshot_key)

    def expire_headshot(self) -> None:
        self.expire(self._public_user_headshot_key)

    def expire(self, key: str) -> None:
        try:
            del self._cache[key]
        except KeyError:
            pass

    def clear(self) -> None:
        self._cache.clear()
        self._cache = {}


Cache = _Cache()
