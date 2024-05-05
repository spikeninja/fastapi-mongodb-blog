from io import BytesIO
from minio import Minio


class FilesService:

    def __init__(self, minio_client: Minio, bucket_name: str):
        self._client = minio_client
        self.bucket_name = bucket_name

    async def put_file(self, file_name: str, content: bytes):
        """"""

        found = self._client.bucket_exists(bucket_name=self.bucket_name)
        if not found:
            self._client.make_bucket(bucket_name=self.bucket_name)

        self._client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_name,
            data=BytesIO(content),
            length=len(content),
        )

    async def get_file(self, file_name: str) -> bytes:
        """"""

        response = self._client.get_object(
            object_name=file_name,
            bucket_name=self.bucket_name,
        )

        return response.data

    def sync_put_file(self, file_name: str, content: bytes):
        """"""

        found = self._client.bucket_exists(bucket_name=self.bucket_name)
        if not found:
            self._client.make_bucket(bucket_name=self.bucket_name)

        self._client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_name,
            data=BytesIO(content),
            length=len(content),
        )

    def sync_get_file(self, file_name: str) -> bytes:
        """"""

        response = self._client.get_object(
            object_name=file_name,
            bucket_name=self.bucket_name,
        )

        return response.data
