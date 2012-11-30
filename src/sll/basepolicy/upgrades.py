from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging


logger = logging.getLogger(__name__)


PROFILE_ID = "profile-sll.basepolicy:default"

# Custom upgrade functions for setuphandlers to run
setups = []


def set_record_abita_development_rate(rate):
    logger.info('Setting record: abita.development.rate to {}'.format(rate))
    getUtility(IRegistry)['abita.development.rate'] = rate


def reimport_profile(context, profile, name):
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting {} with profile: {}.'.format(name, profile))
    setup.runImportStepFromProfile(profile, name, run_dependencies=False, purge_old=False)


def install_packages(context, names):
    """Installs package(s)."""
    installer = getToolByName(context, 'portal_quickinstaller')
    if not isinstance(names, list):
        names = [names]
    for name in names:
        logger.info('Installing {}.'.format(name))
        installer.installProduct(name)
