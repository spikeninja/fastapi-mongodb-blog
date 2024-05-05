from typing import Any, Callable, Union

import bson
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import PydanticOmit, core_schema
from pydantic import SerializerFunctionWrapHandler, GetJsonSchemaHandler


def omit_if_none(v: Any, handler: SerializerFunctionWrapHandler) -> str | None:
    if v is None:
        return handler(PydanticOmit)
    return handler(v)


class PydanticObjectId(bson.ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_string_or_bytes(value: Union[str, bytes]) -> bson.ObjectId:
            try:
                return bson.ObjectId(value)
            except bson.errors.InvalidId:
                raise ValueError("Invalid ObjectId")

        from_string_or_bytes_schema = core_schema.chain_schema(
            [
                core_schema.union_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.bytes_schema(),
                    ]
                ),
                core_schema.no_info_plain_validator_function(
                    validate_from_string_or_bytes
                ),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_string_or_bytes_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(bson.ObjectId),
                    from_string_or_bytes_schema,
                ],
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                str, when_used="json"
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema.str_schema())
        json_schema.update(
            examples=["5f85f36d6dfecacc68428a46", "ffffffffffffffffffffffff"],
            example="5f85f36d6dfecacc68428a46",
        )
        return json_schema
