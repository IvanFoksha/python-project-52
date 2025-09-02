from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    def get_extra_data(self, request, exc):
        extra_data = {
            'trace_id': 'aabbccddeeff',
            'feature_flags': ['feature_1', 'feature_2'],
        }
        return extra_data

    def get_payload_data(self, request, exc):
        payload_data = {}
        if hasattr(request, 'user') and not request.user.is_anonymous:
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'username': request.user.username,
                },
            }
        return payload_data
