import hashlib
import datetime

class AbstractRole:
    _next_id = 1

    def __init__(self, full_name, email, password):
        self._id = AbstractRole._next_id
        AbstractRole._next_id += 1
        self._full_name = full_name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._created_at = datetime.datetime.now().isoformat()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._password_hash == self._hash_password(password)

    def get_profile(self):
        raise NotImplementedError

    def update_profile(self, **kwargs):
        raise NotImplementedError

