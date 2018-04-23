"""multiskel errors"""

class MultiSkelError(Exception):
	pass

class MultiSkelWarning(RuntimeWarning):
	info = "This could be dangerous! See multiskel documentation."

	def __init__(self, message, **kwargs):
		message += " " + self.info
		super().__init__(message, **kwargs)


class SecurityError(MultiSkelError):
	pass

class SecurityWarning(MultiSkelWarning):
	pass