"""multiskel utility functions"""

import collections


def force_list(obj, none_makes_empty_list=True):
	"""
	Forces 'obj' to be a sequence, even if a sequence of only one item

	- Pass it a str, byte, or bytearray and it'll return a 1-element list
	- Pass it a None, and it'll return an empty list
	- Pass it any other kind of sequence and it'll cast it to a list
	- Pass it an object that doesn't register itself as a Sequence, and it'll return
	  a 1-element list of that object
	"""

	if obj is None:
		obj = []
	elif type(obj) is str or type(obj) is byte or type(obj) is bytearray:
		# Got to special case this because these are Sequences
		obj = [ obj ]
	elif isinstance(obj, collections.Sequence):
		pass # obj is already fine!
	else:
		obj = [ obj ]

	return obj
	