from typing import Generator

from miniopy_async import Minio

from core.config import settings


class MinioHelper:
    def __init__(
        self,
        host: str = settings.minio.host,
        access_key: str = settings.minio.access_key,
        secret_key: str = settings.minio.secret_key,
        secure: bool = settings.minio.secure,
    ):
        self.async_client = Minio(
            host,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

    def minio_getter(self) -> Generator[Minio, None]:
        yield self.async_client

    async def create_buckets_if_not_exists(self, buckets: list[str]):
        need_buckets = set(buckets)
        exists = set(bucket.name for bucket in await self.async_client.list_buckets())
        to_create = need_buckets - exists
        if not to_create:
            return
        for bucket_name in to_create:
            await self.async_client.make_bucket(bucket_name=bucket_name)


minio_helper = MinioHelper()
