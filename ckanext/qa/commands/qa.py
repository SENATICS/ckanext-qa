import sys
import os
from pylons import config
from ckan.lib.cli import CkanCommand
from ckan.model import Session, Package, repo
from ckanext.qa.lib.package_scorer import package_score

# Use this specific author so that these revisions can be filtered out of
# normal RSS feeds that cover significant package changes. See DGU#982.
MAINTENANCE_AUTHOR = u'okfn_maintenance'

class QA(CkanCommand):
    """Manage the ratings stored in the db

    Usage::

        paster qa [options] update [{package-id}]
           - Update all package scores or just one if a package id is provided

        paster qa clean        
            - Remove all package score information

    Available options::

        -s {package-id} Start the process from the specified package.
                        (Ignored if a package id is provided as an argument)

        -l {int}        Limit the process to a number of packages.
                        (Ignored if a package id is provided as an argument)

        -o              Force the score update even if it already exists.

    The commands should be run from the ckanext-qa directory and expect
    a development.ini file to be present. Most of the time you will
    specify the config explicitly though::

        paster qa update --config=../ckan/development.ini

    """    
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 2 
    min_args = 0

    existing_dests = [o.dest for o in CkanCommand.parser.option_list]
    if not 'start' in existing_dests:
        CkanCommand.parser.add_option('-s', '--start',
            action='store',
            dest='start',
            default=False,
            help="""Start the process from the specified package.
                    (Ignored if a package id is provided as an argument)"""
        )
    if not 'limit' in existing_dests:
        CkanCommand.parser.add_option('-l', '--limit',
            action='store',
            dest='limit',
            default=False,
            help="""Limit the process to a number of packages.
                    (Ignored if a package id is provided as an argument)"""
        )
    if not 'force' in existing_dests:
        CkanCommand.parser.add_option('-o', '--force',
            action='store_true',
            dest='force',
            default=False,
            help="Force the score update even if it already exists."
        )

    def command(self):
        """
        Parse command line arguments and call appropriate method.
        """
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print QA.__doc__
            return

        self._load_config()
        self.downloads_folder = config['ckan.qa_downloads'] 
        self.archive_folder = config['ckan.qa_archive']
        cmd = self.args[0]
        if cmd == 'update':
            self.update(unicode(self.args[1]) if len(self.args) > 1 else None)
        elif cmd == 'clean':
            self.clean()
        else:
            sys.stderr.write('Command %s not recognized\n' % (cmd,))

    def clean(self):
        """
        Remove all archived resources.
        """
        print "QA Clean: No longer functional"
        # revision = repo.new_revision()
        # revision.author = MAINTENANCE_AUTHOR
        # revision.message = u'Update package scores from cli'
        # for item in Session.query(PackageExtra).filter(PackageExtra.key.in_(PKGEXTRA)).all():
        #     item.purge()
        # repo.commit_and_remove()

    def update(self, package_id = None):
        # check that downloads folder exists
        if not os.path.exists(self.downloads_folder):
            print "Error: No downloads found."
            print "       Check that the downloads path is correct and run the archive command"
            return
        results_file = os.path.join(self.downloads_folder, 'archive.db')

        revision = repo.new_revision()
        revision.author = MAINTENANCE_AUTHOR
        revision.message = u'Update package scores from cli'

        if package_id:
            package = Package.get(package_id)
            if package:
                packages = [package]
            else:
                print "Error: Package not found:", package_id
        else:
            start = self.options.start
            limit = int(self.options.limit or 0)
            if start:
                ids = Session.query(Package.id).order_by(Package.id).all()
                index = [i for i,v in enumerate(ids) if v[0] == start]
                if not index:
                    sys.stderr.write('Error: Package not found: %s \n' % start)
                    sys.exit()
                if limit is not False:
                    ids = ids[index[0]:index[0] + limit]
                else:
                    ids = ids[index[0]:]
                packages = [Session.query(Package).filter(Package.id == id[0]).first() for id in ids]
            else:
                if limit:
                    packages = Session.query(Package).limit(limit).all()
                else:
                    packages = Session.query(Package).all()

        print "Total packages to update: " + str(len(packages))
        for package in packages:
            print "Checking package", package.id, package.name
            for resource in package.resources:
                print '\t%s' % (resource.url,)
            package_score(package, results_file)
        repo.commit()
        repo.commit_and_remove()
