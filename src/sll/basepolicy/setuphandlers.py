import logging


def setupVarious(context):

    if context.readDataFile('sll.basepolicy_various.txt') is None:
        return

    portal = context.getSite()
    logger = logging.getLogger(__name__)

    from sll.basepolicy.upgrades import setups
    for setup_func in setups:
        setup_func(portal, logger)
