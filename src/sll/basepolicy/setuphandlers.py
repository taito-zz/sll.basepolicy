from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger(__name__)


def set_firstweekday(context):
    calendar = getToolByName(context, 'portal_calendar')
    logger.info('Setting first weekday to Monday.')
    calendar.firstweekday = 0


def setupVarious(context):

    if context.readDataFile('sll.basepolicy_various.txt') is None:
        return

    portal = context.getSite()
    set_firstweekday(portal)
