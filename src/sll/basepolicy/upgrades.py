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


def install_packages(context, names):
    """Installs package(s)."""
    installer = getToolByName(context, 'portal_quickinstaller')
    if not isinstance(names, list):
        names = [names]
    for name in names:
        logger.info('Installing {}.'.format(name))
        installer.installProduct(name)


def install_sll_basepolicy(context):
    """Intall sll.basepolicy"""
    install_packages(context, 'sll.basepolicy')


def reimport_registry(setup):
    """Reimport plone.app.registry"""
    setup.runImportStepFromProfile('profile-sll.basepolicy:default', 'plone.app.registry', run_dependencies=False, purge_old=False)
