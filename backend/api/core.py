from django.template import loader
from django.core.cache import cache
from django.utils import timezone
from rest_framework.filters import BaseFilterBackend
from rest_framework.throttling import BaseThrottle


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


class BotThrottle(BaseThrottle):
    """
    Custom throttle that allows 60 requests per minute, then blocks for 1 hour.
    Designed to prevent bot flooding while allowing legitimate use.
    """
    rate = '60/min'  # 60 requests per minute
    block_duration = 3600  # 1 hour in seconds
    
    def get_cache_key(self, request, view):
        """Generate cache key based on IP address"""
        ident = self.get_ident(request)
        return f'throttle_bot_{ident}'
    
    def get_block_key(self, request, view):
        """Generate cache key for block status"""
        ident = self.get_ident(request)
        return f'throttle_block_{ident}'
    
    def allow_request(self, request, view):
        """
        Check if request should be allowed.
        Returns True if allowed, False if throttled.
        """
        # First check if IP is blocked
        block_key = self.get_block_key(request, view)
        blocked_until = cache.get(block_key)
        
        if blocked_until:
            # Check if block has expired
            if timezone.now().timestamp() < blocked_until:
                # Still blocked
                return False
            else:
                # Block expired, remove it
                cache.delete(block_key)
        
        # Check current request rate
        key = self.get_cache_key(request, view)
        history = cache.get(key, [])
        now = timezone.now().timestamp()
        
        # Remove requests older than 1 minute
        history = [h for h in history if now - h < 60]
        
        # Check if limit exceeded
        if len(history) >= 60:
            # Block for 1 hour
            block_until = now + self.block_duration
            cache.set(block_key, block_until, self.block_duration)
            return False
        
        # Add current request to history
        history.append(now)
        cache.set(key, history, 60)  # Cache for 1 minute
        
        return True
    
    def wait(self):
        """
        Return the number of seconds to wait before retrying.
        This is called when allow_request returns False.
        """
        # For blocked users, return the remaining block time
        # This is a simplified version - in practice, we'd need to pass request/view
        # For now, return a reasonable wait time
        return self.block_duration

