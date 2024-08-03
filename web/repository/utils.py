from typing import Type
from operator import eq, ne, ge, gt, le, lt

from odmantic import query, Model
from odmantic.query import QueryExpression

sorters_map = {
    "asc": query.asc,
    "desc": query.desc,
}

operators_map = {
    "eq": eq,
    "ne": ne,
    "ge": ge,
    "gt": gt,
    "le": le,
    "lt": lt,
    "in": query.in_,
}


async def apply_filters(
    model: Type[Model],
    filters: list[dict] | None,
) -> QueryExpression:
    """"""

    filters_query = QueryExpression()

    if filters:
        for _filter in filters:
            operation = operators_map[_filter['operation']]
            filters_query &= (
                operation(
                    getattr(model, _filter['field']),
                    _filter['val'],
                )
            )

    return filters_query


async def apply_sorters(
    model: Type[Model],
    sorters: list[dict] | None,
) -> tuple | None:
    """"""

    if not sorters:
        return None

    sorters_clauses = []
    if sorters:
        for sorter in sorters:
            op = sorters_map[sorter['order']]
            sorters_clauses.append(
                op(
                    getattr(model, sorter['field'])
                )
            )

    return tuple(sorters_clauses)
