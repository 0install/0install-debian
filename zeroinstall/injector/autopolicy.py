import os
from logging import debug, info

from zeroinstall.injector import model, download
from zeroinstall.injector import policy, run, handler

class NeedDownload(Exception):
	"""Thrown if we tried to start a download with allow_downloads = False"""
	def __init__(self, url):
		Exception.__init__(self, "Would download '%s'" % url)

class AutoPolicy(policy.Policy):
	allow_downloads = False
	download_only = False
	dry_run = False

	def __init__(self, interface_uri, download_only = False, dry_run = False):
		if not interface_uri.startswith('http:'):
			interface_uri = os.path.realpath(interface_uri)	# For testing
		policy.Policy.__init__(self, interface_uri, handler.Handler())
		self.dry_run = dry_run
		self.allow_downloads = not dry_run
		self.download_only = download_only
		self.dry_run = dry_run
	
	def need_download(self):
		"""Decide whether we need to download anything (but don't do it!)"""
		old = self.allow_downloads
		self.allow_downloads = False
		try:
			try:
				self.recalculate()
				debug("Recalculated: ready = %s", self.ready)
				if not self.ready: return False
				self.start_downloading_impls()
			except NeedDownload:
				return True
			return False
		finally:
			self.allow_downloads = old
	
	def begin_iface_download(self, interface, force = False):
		if self.dry_run or not self.allow_downloads:
			raise NeedDownload(interface.uri)
		else:
			policy.Policy.begin_iface_download(self, interface, force)

	def start_downloading_impls(self):
		for iface, impl in self.get_uncached_implementations():
			debug("start_downloading_impls: for %s get %s", iface, impl)
			if not impl.download_sources:
				raise model.SafeException("Implementation " + impl.id + " of "
					"interface " + iface.get_name() + " cannot be "
					"downloaded (no download locations given in "
					"interface!")
			source = impl.download_sources[0]
			if self.dry_run or not self.allow_downloads:
				raise NeedDownload(source.url)
			else:
				dl = download.begin_impl_download(source)
				self.handler.monitor_download(dl)

	def execute(self, prog_args):
		self.start_downloading_impls()
		self.handler.wait_for_downloads()
		if not self.download_only:
			run.execute(self, prog_args, dry_run = self.dry_run)
		else:
			info("Downloads done (download-only mode)")
	
	def recalculate_with_dl(self):
		self.recalculate()
		if self.handler.monitored_downloads:
			self.handler.wait_for_downloads()
			self.recalculate()
	
	def download_and_execute(self, prog_args, refresh = False):
		self.recalculate_with_dl()
		if refresh:
			self.refresh_all(False)
			self.recalculate_with_dl()
		if not self.ready:
			raise model.SafeException("Can't find all required implementations:\n" +
				'\n'.join(["- %s -> %s" % (iface, impl)
					   for iface, impl in self.walk_implementations()]))
		self.execute(prog_args)
