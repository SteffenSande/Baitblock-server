from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin(object):
    """
    A mixin object that let's a django rest framework view have multiple lookup fields
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object
