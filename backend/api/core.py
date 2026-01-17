from django.template import loader

from rest_framework.filters import BaseFilterBackend


class QueryFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        for field in view.query_filters:
            values = self.get_param(request, field)
            filter_method = getattr(view, "filter_" + field, None)
            if filter_method:
                queryset = filter_method(request, queryset, values)
            elif values:
                queryset = queryset.filter(**{field + "__in": values})
        return queryset

    def get_schema_operation_parameters(self, view):
        schema = []
        for field in view.query_filters:
            if (
                view.serializer_class
                and isinstance(view.serializer_class().get_fields(), dict)
                and field in view.serializer_class().get_fields()
            ):
                serializer_field = view.serializer_class().get_fields()[field]
                schema.append(
                    {
                        "name": field,
                        "required": serializer_field.required,
                        "in": "query",
                        "schema": {"type": "string"},
                        "serializer": view.serializer_class(),
                    }
                )
            else:
                schema.append({"name": field, "required": False, "in": "query", "schema": {"type": "string"}})
        return schema

    @classmethod
    def get_param(self, request, field):
        raw_values = request.query_params.getlist(field)
        return list(filter(bool, raw_values))


