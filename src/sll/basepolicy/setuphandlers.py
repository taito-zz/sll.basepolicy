from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger(__name__)


def exclude_from_nav(context):
    """Object exclude from nav."""
    portal = context.getSite()
    ids = ['Members', 'events', 'news']
    for oid in ids:
        obj = portal.get(oid)
        logger.info('Excluding from navigation: {}'.format('/'.join(obj.getPhysicalPath())))
        obj.setExcludeFromNav(True)
        obj.reindexObject()


def remove_front_page(context):
    logger.info('Removing front-page.')
    context.manage_delObjects(['front-page'])


def remove_skin(context, names):
    """Removes skin by name."""
    skins = getToolByName(context, 'portal_skins')
    skins.manage_skinLayers(chosen=names, del_skin=True)


def set_firstweekday(context):
    calendar = getToolByName(context, 'portal_calendar')
    logger.info('Setting first weekday to Monday.')
    calendar.firstweekday = 0


def uninstall_package(context, packages):
    """Uninstall packages.

    :param packages: List of package names.
    :type packages: list
    """
    installer = getToolByName(context, 'portal_quickinstaller')
    packages = [package for package in packages if installer.isProductInstalled(package)]
    logger.info('Uninstalling {}'.format(', '.join(packages)))
    installer.uninstallProducts(packages)


def setupVarious(context):

    if context.readDataFile('sll.basepolicy_various.txt') is None:
        return

    portal = context.getSite()
    exclude_from_nav(context)
    remove_front_page(portal)
    remove_skin(portal, ('Plone Default', ))
    set_firstweekday(portal)
    uninstall_package(portal, ['plonetheme.classic'])
