from genshi.builder import tag

from trac.core import Component
from trac.timeline.api import ITimelineEventProvider
from trac.wiki.formatter import format_to, format_to_html, format_to_oneliner
from trac.util.translation import _, tag_

from api import BuildBotSystem

class TracBuildBotWatcher(Component):
	implements(ITimelineEventProvider)
	buildbot = Option('bbwatcher', 'buildmaster', '127.0.0.1:8080')

	# Timeline Methods
	def get_timeline_filters(self, req):
		yield ('bbwatcher', 'Builds')
	def get_timeline_events(self, req, start, stop, filters):
		if not 'bbwatcher' in filters:
			return
		master = BuildBotSystem(self.env)
		# This was a comprehension: the loop is clearer
		for build in master.getAllBuildsInInterval(start, stop):
			# BuildBot builds are reported as
			# (builder_name, num, end, branch, rev, results, text)
			yield ('build', mktime(build[2]), '', build)
	def render_timeline_event(self, context, field, event):
		builder_name, num, end, branch, rev, results, text = event[3]
		if field == 'url':
			return context.href.changeset(rev)
		elif field == 'title':
			return tag_('Build %(num)s of %(builder)s %(verb)s',
				num=tag.em('#', num=num), builder=builder_name,
				verb=(results == 'success' and 'passed' or 'failed'))
