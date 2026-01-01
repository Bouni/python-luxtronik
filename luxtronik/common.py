from threading import RLock

# Global lock to synchronize access to the hosts_locks dictionary
_management_lock = RLock()
_hosts_locks = {}

def get_host_lock(host):
    """
    Retrieve the unique lock object associated with a given host.
    The same thread can acquire a RLock as often as desired.

    If no lock exists for the host, a new one is created in a thread-safe manner.

    Args:
        host (str): Hostname or IP address.

    Returns:
        RLock: The lock object dedicated to the given host.
    """
    # Ensure a dedicated lock is created for each IP.
    with _management_lock:
        if host not in _hosts_locks:
            _hosts_locks[host] = RLock()
        return _hosts_locks[host]

class classproperty:
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, instance, owner):
        return self.fget(owner)
