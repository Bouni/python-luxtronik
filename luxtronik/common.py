
from threading import RLock

###############################################################################
# Multi-threading lock mechanism
###############################################################################

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

###############################################################################
# Class property
###############################################################################

class classproperty:
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, instance, owner):
        return self.fget(owner)

###############################################################################
# Version methods
###############################################################################

def parse_version(version):
    """
    Parse a version string into a tuple with exactly 4 integers.
    The individual numbers correspond to `major.minor.patch.build`.
    A given tuple of integers is expanded or reduced to 4 integers.

    Examples:
        "1"         -> (1, 0, 0, 0)
        "2.1"       -> (2, 1, 0, 0)
        "3.2.1"     -> (3, 2, 1, 0)
        "1.2.3.4"   -> (1, 2, 3, 4)
        "1.2.3.4.5" -> (1, 2, 3, 4)   # extra parts are ignored
        "a.b"       -> None

    Args:
        version (str | tuple[int, ...]): Version string or version as tuple.

    Returns:
        tuple[int, int, int, int] | None: Parsed version tuple, or None if invalid.
    """
    if isinstance(version, tuple) and all(type(p) is int for p in version):
        return (version + (0, 0, 0, 0))[:4]
    elif isinstance(version, str):
        parts = version.strip().split(".")
        if not parts or any(not p.isdigit() for p in parts):
            return None
        nums = [int(p) for p in parts]
        nums = (nums + [0, 0, 0, 0])[:4]
        return tuple(nums)
    else:
        return None


def version_in_range(version, since=None, until=None):
    """
    Check whether a version is within the specified range of `[since..until]`.
    If an argument is None, the corresponding check is skipped.

    Args:
        version (tuple[int, ...] | None): The version to check.
            If None, returns True.
        since (tuple[int, ...] | None): Lower bound (inclusive).
            If None, no lower bound is applied.
        until (tuple[int, ...] | None): Upper bound (inclusive).
            If None, no upper bound is applied.

    Returns:
        bool: True if version is within the range, False otherwise.
    """
    if version is None:
        return True
    if since is not None and version < since:
        return False
    if until is not None and version > until:
        return False
    return True
