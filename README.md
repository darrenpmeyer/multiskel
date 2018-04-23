# multiskel

Define and use 'skeleton templates' (skels) for various project types


# Installation

	git clone https://github.com/darrenpmeyer/multiskel.git ~/.multiskel

Add `~/.multiskel/bin` to your `PATH` from inside your `.bashrc` or equivalent for best results.

# Use

	mskel [-I<include_dir>] SKEL [target]

		SKEL      The name of a skel to clone
		-I        Add directories to search for skels, separated by ':'
		target    directory to clone to -- defaults to current directory

To add more skels, you may either place them in `~/.multiskel/installed/` or add them from repositories using then `addskel` utility:

	addskel [method] pathspec [name]

		method    How to acquire the repository. Currently 'hg' and 'git' are supported
		pathspec  the path to the repository; can be a URL or service spec
		name      the name to give the installed skel

If `method` is not provided, it will be guessed from the `pathspec`; if that's not possible, we assume `git`

The name of the installed skel, if not specified, will be the final component of the path, minus any extensions and leading `skel-`. Examples:

	/path/to/java-servlet                        =>  java-servlet
	/path/to/skel-java-app                       =>  java-app
	https://domain.tld/skels/skel-java-bean.git  =>  java-bean

A skel may also override the default name in its `config.skel` file; you will be warned if this happens. Settings in `config.skel` **do not** override names specified on the command line.



## Service specifications for pathspec

Pathspec can be a URL directly to a repository endpoint, but it can also be a "service spec" -- a shorthand for common distribution point services like github and bitbucket.

Service specfications are in the form `[service:]service_path`; for example:

	github:darrenpmeyer/skel-python-app

Would point to the `skel-python-app` skep from github user `darrenpmeyer`. 

If no service name is supplied, the service will be resolved by trying the following, with the first match being used:

1. treat it as a local filesystem path
2. treat it as a github service path
3. treat it as a bitbucket service path



# License

(c) 2018 Darren P Meyer <https://github.com/darrenpmeyer>

(contributors, please add your copyright information above)

Use, distribution, and modification is permitted under the terms of GNU Lesser General Public License v3.0 (LGPL 3.0), the text of which is available from the file [`LICENSE`](LICENSE) or from [the GNU website](https://www.gnu.org/licenses/lgpl-3.0.en.html). All other rights not granted by the license are reserved.
