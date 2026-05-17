from django.contrib.auth.mixins import UserPassesTestMixin


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return getattr(self.request.user, 'role', None) == 'MANAGER'
