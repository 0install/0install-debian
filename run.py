import os, sys

from model import *

def do_env_binding(binding, path):
	extra = os.path.join(path, binding.insert)
	if binding.name in os.environ:
		os.environ[binding.name] = extra + ':' + os.environ[binding.name]
	else:
		os.environ[binding.name] = extra
	#print "%s=%s" % (binding.name, os.environ[binding.name])

def execute(policy, prog, prog_args):
	iface = policy.get_interface(policy.root)
	def setup_bindings(i):
		impl = policy.get_implementation(i)
		for dep in impl.dependencies.values():
			dep_iface = policy.get_interface(dep.interface)
			for b in dep.bindings:
				if isinstance(b, EnvironmentBinding):
					dep_impl = policy.get_implementation(dep_iface)
					do_env_binding(b, policy.get_implementation_path(dep_impl))
			setup_bindings(dep_iface)
	setup_bindings(iface)
	
	root_impl = policy.get_implementation(iface)
	prog_path = os.path.join(policy.get_implementation_path(root_impl), prog)
	if not os.path.exists(prog_path):
		print >>sys.stderr, "'%s' does not exist." % prog_path
		print >>sys.stderr, "(implementation '%s' + program '%s')" % (policy.implementation[iface].path, prog)
		sys.exit(1)
	os.execl(prog_path, prog_path, *prog_args)
