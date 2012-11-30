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
