"""multiskel recursively copy feature"""

import logging
import os, re, shutil, enum, warnings

from multiskel.util import force_list
from multiskel.error import SecurityError, SecurityWarning


def copy(src, dst_root, recurse=True, exclude=None, relink_symlinks=None, resolve_symlinks=None):
	exclude = force_list(exclude)
	relink_symlinks = force_list(relink_symlinks)
	resolve_symlinks = force_list(resolve_symlinks)

	copied_files = []
	if any_pattern_matches(src, *exclude):
		return copied_files

	# resolve what to do if this is a symlink
	# by default - skip and raise error
	follow_symlinks = False  
	if os.path.islink(src):
		if any_pattern_matches(src, *relink_symlinks):
			warnings.warn(
				"{} is a symlink, we are copying it as a symlink. ".format(src),
				SecurityWarning)
			follow_symlinks = False # causes isfile() test below to copy the link as a link
		elif any_pattern_matches(src, *resolve_symlinks):
			warnings.warn(
				"{} is a symlink, we are copying it as a full path. ".format(src),
				SecurityWarning)
			follow_symlinks = True # causes isfile() test below to copy the link as a file
		else:
			raise SecurityError("'{}' is a symlink".format(src))

	# what to do if src is a file. Something can be both a symlink and a file!
	if os.path.isfile(src):
		target = shutil.copy(src, dst_root, follow_symlinks=follow_symlinks)
		copied_files.append((src, target))  # appends a tuple to the copied_files list

	# what to do if src is a directory. Something can be both a symlink and a directory!
	if os.path.isdir(src):
		target_mode = os.stat(os.path.realpath(src)).st_mode

		if follow_symlinks or not os.path.islink(src):
			newdst_root = os.join(dst_root, os.path.basename(src))
			os.makedirs(newdst_root, mode=target_mode, exist_ok=True)

			if recurse:
				for path in os.listdir(src):
					copied = copy(path, newdst_root, recurse, exclude, relink_symlinks, resolve_symlinks)
					copied_files.extend(copied)
			else:
				pass  # TODO do we say something about skipped directories?
		else:
			# if this is a symlink and we aren't supposed to follow them, then we
			# create a new link to the same destination
			linksrc = os.readlink(src)
			linkdst = dst_root

			if os.isdir(linkdst):
				linkdst = os.path.join(lindst, os.path.basename(src))

			os.symlink(linksrc, linkdst)

	return copied_files


def any_pattern_matches(candidate, *patterns):
	for pattern in patterns:
		if not isinstance(pattern, Pattern):
			pattern = Pattern(pattern)

		if pattern.matches(candidate):
			return True

	return False


class Pattern(object):
	compiled_pattern = type(re.compile(''))  # for type comparisons

	def __init__(self, pattern):
		self.pattern = pattern

	def matches(self, candidate):
		does_match = False

		if type(self.pattern) is self.compiled_pattern and self.pattern.search(candidate):
			does_match = True
		elif self.pattern == candidate:
			does_match = True

		return does_match


class Mode(enum.Enum):
	AS_LINK = 1
	AS_FILE = 2