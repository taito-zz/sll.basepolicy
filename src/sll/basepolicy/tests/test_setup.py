from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from sll.basepolicy.tests.base import IntegrationTestCase


def get_record(name):
    from zope.component import getUtility
    from plone.registry.interfaces import IRegistry
    return getUtility(IRegistry).records.get(name)


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_sll_basepolicy__installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('sll.basepolicy'))

    def test_jsregistry__popupforms(self):
        javascripts = getToolByName(self.portal, 'portal_javascripts')
        resource = javascripts.getResource('popupforms.js')
        self.assertFalse(resource.getEnabled())

    def test_mailhost__smtp_host(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_host, 'sll.fi')

    def test_mailhost__smtp_port(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_port, 25)

    def test_metadata__dependency__abita_development(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.development'))

    def test_metadata__dependency__hexagonit_socialbutton(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('hexagonit.socialbutton'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-sll.basepolicy:default'), u'0')

    def test_memberdata_properties__wysiwyg_editor(self):
        membership = getToolByName(self.portal, 'portal_membership')
        member = membership.getMemberById(TEST_USER_ID)
        self.assertEqual(member.getProperty('wysiwyg_editor'), 'TinyMCE')

    def test_memberdata_properties__visible_ids(self):
        membership = getToolByName(self.portal, 'portal_membership')
        member = membership.getMemberById(TEST_USER_ID)
        self.assertTrue(member.getProperty('visible_ids'))

    def get_property(self, category, name):
        return getattr(getToolByName(self.portal, 'portal_properties'), category).getProperty(name)

    def test_propertiestool__navtree_properties__metaTypesNotToList(self):
        number_of_default_ctypes = 17
        additional_ctypes = ('Collection', 'Event', 'File', 'Image', 'Link', 'Topic')
        ctypes = self.get_property('navtree_properties', 'metaTypesNotToList')
        self.assertEqual(len(ctypes), number_of_default_ctypes + len(additional_ctypes))
        for ctype in additional_ctypes:
            self.assertIn(ctype, ctypes)

    def test_propertiestool__site_properties__available_editors(self):
        self.assertEqual(self.get_property('site_properties', 'available_editors'), ('TinyMCE',))

    def test_propertiestool__site_properties__default_language(self):
        self.assertEqual(self.get_property('site_properties', 'default_language'), 'fi')

    def test_propertiestool__site_properties__enable_sitemap(self):
        self.assertTrue(self.get_property('site_properties', 'enable_sitemap'))

    def test_propertiestool__site_properties__external_links_open_new_window(self):
        self.assertEqual(self.get_property('site_properties', 'external_links_open_new_window'), 'true')

    def test_propertiestool__site_properties__types_not_searched(self):
        number_of_default_ctypes = 17
        additional_ctypes = ('Collection', 'Topic')
        ctypes = self.get_property('site_properties', 'types_not_searched')
        self.assertEqual(len(ctypes), number_of_default_ctypes + len(additional_ctypes))
        for ctype in additional_ctypes:
            self.assertIn(ctype, ctypes)

    def test_propertiestool__site_properties__icon_visibility(self):
        self.assertEqual(self.get_property('site_properties', 'icon_visibility'), 'authenticated')

    def test_propertiestool__site_properties__use_email_as_login(self):
        self.assertTrue(self.get_property('site_properties', 'use_email_as_login'))

    def test_propertiestool__site_properties__visible_ids(self):
        self.assertTrue(self.get_property('site_properties', 'visible_ids'))

    def test_registry_record_hexagonit_socialbutton_codes(self):
        record = get_record('hexagonit.socialbutton.codes')
        self.assertEqual(record.value, {
            u'twitter': {u'code_text': u'<a class="social-button twitter" title="Twitter" href="https://twitter.com/share?text=${title}?url=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/twitter.gif" />\n</a>'},
            u'facebook': {u'code_text': u'<a class="social-button facebook" title="Facebook" target="_blank" href="http://www.facebook.com/sharer.php?t=${title}&u=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/facebook.gif" />\n</a>'},
            u'google-plus': {u'code_text': u'<a class="social-button googleplus" title="Google+" href="https://plusone.google.com/_/+1/confirm?hl=${lang}&title=${title}&url=${url}">\n<img src="${portal_url}/++resource++hexagonit.socialbutton/google-plus.gif" />\n</a>'},
        })

    def test_registry_record_hexagonit_socialbutton_config(self):
        record = get_record('hexagonit.socialbutton.config')
        self.assertEqual(record.value, {
            u'twitter': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'facebook': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
            u'google-plus': {u'content_types': u'Document,Folder,FormFolder,Plone Site,News Item,Event', u'view_permission_only': u'True', u'view_models': u'*', u'enabled': u'True', u'viewlet_manager': u'plone.belowcontent'},
        })

    def get_roles(self, obj, permission):
        return sorted([item['name'] for item in obj.rolesOfPermission(permission) if item['selected'] == 'SELECTED'])

    def test_rolemap__Manage_portlets__rolesOfPermission(self):
        permission = "Portlets: Manage portlets"
        self.assertEqual(self.get_roles(self.portal, permission), [
            'Editor',
            'Manager',
            'Site Administrator'])

    def test_rolemap__Manage_portlets__acquiredRolesAreUsedBy(self):
        permission = "Portlets: Manage portlets"
        self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), 'CHECKED')

    def test_rolemap__Manage_own_portlets__rolesOfPermission(self):
        permission = "Portlets: Manage own portlets"
        self.assertEqual(self.get_roles(self.portal, permission), [
            'Editor',
            'Manager',
            'Site Administrator'])

    def test_rolemap__Manage_own_portlets__acquiredRolesAreUsedBy(self):
        permission = "Portlets: Manage own portlets"
        self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), 'CHECKED')

    def test_rolemap__Add_collection_portlet__rolesOfPermission(self):
        permission = "plone.portlet.collection: Add collection portlet"
        self.assertEqual(self.get_roles(self.portal, permission), [
            'Editor',
            'Manager',
            'Site Administrator'])

    def test_rolemap__Add_collection_portlet__acquiredRolesAreUsedBy(self):
        permission = "plone.portlet.collection: Add collection portlet"
        self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), 'CHECKED')

    def test_rolemap__Add_static_portlet__rolesOfPermission(self):
        permission = "plone.portlet.static: Add static portlet"
        self.assertEqual(self.get_roles(self.portal, permission), [
            'Editor',
            'Manager',
            'Site Administrator'])

    def test_rolemap__Add_static_portlet__acquiredRolesAreUsedBy(self):
        permission = "plone.portlet.static: Add static portlet"
        self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), 'CHECKED')

    def test_setuphanlders__set_firstweekday(self):
        calendar = getToolByName(self.portal, 'portal_calendar')
        self.assertEqual(calendar.firstweekday, 0)

    def test_tinymce__link_using_uids(self):
        tinymce = getToolByName(self.portal, 'portal_tinymce')
        self.assertTrue(tinymce.link_using_uids)

    def test_workflow__default(self):
        workflow = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(workflow._default_chain, ('two_states_workflow',))

    def get_workflow(self, name):
        workflow = getToolByName(self.portal, 'portal_workflow')
        return workflow[name]

    def test_workflows__two_states_workflow__description(self):
        workflow = self.get_workflow('two_states_workflow')
        self.assertEqual(workflow.description, 'Either Private or Published state.')

    def test_workflows__two_states_workflow__initial_state(self):
        workflow = self.get_workflow('two_states_workflow')
        self.assertEqual(workflow.initial_state, 'private')

    def test_workflows__two_states_workflow__manager_bypass(self):
        workflow = self.get_workflow('two_states_workflow')
        self.assertFalse(workflow.manager_bypass)

    def test_workflows__two_states_workflow__state_variable(self):
        workflow = self.get_workflow('two_states_workflow')
        self.assertEqual(workflow.state_var, 'review_state')

    def test_workflows__two_states_workflow__title(self):
        workflow = self.get_workflow('two_states_workflow')
        self.assertEqual(workflow.title, 'Two States Workflow')

    def test_workflows__two_states_workflow__permissions(self):
        workflow = self.get_workflow('two_states_workflow')
        self.assertEqual(workflow.permissions, (
            'Access contents information',
            'Modify portal content',
            'View'))

    def test_workflows__two_states_workflow__states__private__title(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.private
        self.assertEqual(state.title, 'Private')

    def test_workflows__two_states_workflow__states__private__description(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.private
        self.assertEqual(state.description, '')

    def test_workflows__two_states_workflow__states__private__permission__Access_contents_information(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.private
        self.assertEqual(state.getPermissionInfo('Access contents information'), {
            'acquired': 0,
            'roles': ['Contributor', 'Editor', 'Manager', 'Owner', 'Site Administrator'],
        })

    def test_workflows__two_states_workflow__states__private__permission__Modify_portal_content(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.private
        self.assertEqual(state.getPermissionInfo('Modify portal content'), {
            'acquired': 0,
            'roles': ['Contributor', 'Editor', 'Manager', 'Owner', 'Site Administrator'],
        })

    def test_workflows__two_states_workflow__states__private__permission__View(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.private
        self.assertEqual(state.getPermissionInfo('View'), {
            'acquired': 0,
            'roles': ['Contributor', 'Editor', 'Manager', 'Owner', 'Site Administrator'],
        })

    def test_workflows__two_states_workflow__states__published__title(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.published
        self.assertEqual(state.title, 'Published')

    def test_workflows__two_states_workflow__states__published__description(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.published
        self.assertEqual(state.description, '')

    def test_workflows__two_states_workflow__states__published__permission__Access_contents_information(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.published
        self.assertEqual(state.getPermissionInfo('Access contents information'), {
            'acquired': 0,
            'roles': ['Anonymous', 'Authenticated', 'Contributor', 'Editor', 'Manager', 'Owner', 'Site Administrator'],
        })

    def test_workflows__two_states_workflow__states__published__permission__Modify_portal_content(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.published
        self.assertEqual(state.getPermissionInfo('Modify portal content'), {
            'acquired': 0,
            'roles': ['Contributor', 'Editor', 'Manager', 'Owner', 'Site Administrator'],
        })

    def test_workflows__two_states_workflow__states__published__permission__View(self):
        workflow = self.get_workflow('two_states_workflow')
        state = workflow.states.published
        self.assertEqual(state.getPermissionInfo('View'), {
            'acquired': 0,
            'roles': ['Anonymous', 'Authenticated', 'Contributor', 'Editor', 'Manager', 'Owner', 'Site Administrator'],
        })

    def test_workflows__two_states_workflow__transitions__hide__after_script(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.after_script_name, '')

    def test_workflows__two_states_workflow__transitions__hide__before_script(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.script_name, '')

    def test_workflows__two_states_workflow__transitions__hide__new_state(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.new_state_id, 'private')

    def test_workflows__two_states_workflow__transitions__hide__title(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.title, 'Make private')

    def test_workflows__two_states_workflow__transitions__hide__trigger(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.trigger_type, 1)

    def test_workflows__two_states_workflow__transitions__hide__description(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.description, 'Making an item private means that it will not be visible to non-authorized members.')

    def test_workflows__two_states_workflow__transitions__hide__action__category(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.actbox_category, 'workflow')

    def test_workflows__two_states_workflow__transitions__hide__action__icon(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.actbox_icon, '')

    def test_workflows__two_states_workflow__transitions__hide__action__url(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.actbox_url,
            '%(content_url)s/content_status_modify?workflow_action=hide')

    def test_workflows__two_states_workflow__transitions__hide__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.hide
        self.assertEqual(transition.guard.permissions, ('Modify portal content',))

    def test_workflows__two_states_workflow__transitions__publish__after_script(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.after_script_name, '')

    def test_workflows__two_states_workflow__transitions__publish__before_script(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.script_name, '')

    def test_workflows__two_states_workflow__transitions__publish__new_state(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.new_state_id, 'published')

    def test_workflows__two_states_workflow__transitions__publish__title(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.title, 'Publish')

    def test_workflows__two_states_workflow__transitions__publish__trigger(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.trigger_type, 1)

    def test_workflows__two_states_workflow__transitions__publish__description(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.description, 'Publishing the item makes it visible to other users.')

    def test_workflows__two_states_workflow__transitions__publish__action__category(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.actbox_category, 'workflow')

    def test_workflows__two_states_workflow__transitions__publish__action__icon(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.actbox_icon, '')

    def test_workflows__two_states_workflow__transitions__publish__action__url(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.actbox_url,
            '%(content_url)s/content_status_modify?workflow_action=publish')

    def test_workflows__two_states_workflow__transitions__publish__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        transition = workflow.transitions.publish
        self.assertEqual(transition.guard.permissions, ('Modify portal content',))

    def test_workflows__two_states_workflow__variables__action__for_catalog(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.action
        self.assertFalse(variable.for_catalog)

    def test_workflows__two_states_workflow__variables__action__for_status(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.action
        self.assertTrue(variable.for_status)

    def test_workflows__two_states_workflow__variables__action__updata_always(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.action
        self.assertTrue(variable.update_always)

    def test_workflows__two_states_workflow__variables__action__description(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.action
        self.assertEqual(variable.description, 'Previous transition')

    def test_workflows__two_states_workflow__variables__action__default(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.action
        self.assertEqual(variable.getDefaultExprText(), 'transition/getId|nothing')

    def test_workflows__two_states_workflow__variables__action__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.action
        self.assertIsNone(variable.info_guard)

    def test_workflows__two_states_workflow__variables__actor__for_catalog(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.actor
        self.assertFalse(variable.for_catalog)

    def test_workflows__two_states_workflow__variables__actor__for_status(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.actor
        self.assertTrue(variable.for_status)

    def test_workflows__two_states_workflow__variables__actor__updata_always(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.actor
        self.assertTrue(variable.update_always)

    def test_workflows__two_states_workflow__variables__actor__description(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.actor
        self.assertEqual(variable.description, 'The ID of the user who performed the last transition')

    def test_workflows__two_states_workflow__variables__actor__default(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.actor
        self.assertEqual(variable.getDefaultExprText(), 'user/getId')

    def test_workflows__two_states_workflow__variables__actor__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.actor
        self.assertIsNone(variable.info_guard)

    def test_workflows__two_states_workflow__variables__comments__for_catalog(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.comments
        self.assertFalse(variable.for_catalog)

    def test_workflows__two_states_workflow__variables__comments__for_status(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.comments
        self.assertTrue(variable.for_status)

    def test_workflows__two_states_workflow__variables__comments__updata_always(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.comments
        self.assertTrue(variable.update_always)

    def test_workflows__two_states_workflow__variables__comments__description(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.comments
        self.assertEqual(variable.description, 'Comment about the last transition')

    def test_workflows__two_states_workflow__variables__comments__default(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.comments
        self.assertEqual(variable.getDefaultExprText(),
            "python:state_change.kwargs.get('comment', '')")

    def test_workflows__two_states_workflow__variables__comments__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.comments
        self.assertIsNone(variable.info_guard)

    def test_workflows__two_states_workflow__variables__review_history__for_catalog(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.review_history
        self.assertFalse(variable.for_catalog)

    def test_workflows__two_states_workflow__variables__review_history__for_status(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.review_history
        self.assertFalse(variable.for_status)

    def test_workflows__two_states_workflow__variables__review_history__updata_always(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.review_history
        self.assertFalse(variable.update_always)

    def test_workflows__two_states_workflow__variables__review_history__description(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.review_history
        self.assertEqual(variable.description, 'Provides access to workflow history')

    def test_workflows__two_states_workflow__variables__review_history__default(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.review_history
        self.assertEqual(variable.getDefaultExprText(),
            "state_change/getHistory")

    def test_workflows__two_states_workflow__variables__review_history__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.review_history
        self.assertEqual(variable.info_guard.permissions,
            ('Request review', 'Review portal content'))

    def test_workflows__two_states_workflow__variables__time__for_catalog(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.time
        self.assertFalse(variable.for_catalog)

    def test_workflows__two_states_workflow__variables__time__for_status(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.time
        self.assertTrue(variable.for_status)

    def test_workflows__two_states_workflow__variables__time__updata_always(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.time
        self.assertTrue(variable.update_always)

    def test_workflows__two_states_workflow__variables__time__description(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.time
        self.assertEqual(variable.description, 'When the previous transition was performed')

    def test_workflows__two_states_workflow__variables__time__default(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.time
        self.assertEqual(variable.getDefaultExprText(),
            "state_change/getDateTime")

    def test_workflows__two_states_workflow__variables__time__guard(self):
        workflow = self.get_workflow('two_states_workflow')
        variable = workflow.variables.time
        self.assertIsNone(variable.info_guard)

    def test_uninstall(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.basepolicy'])
        self.assertFalse(installer.isProductInstalled('sll.basepolicy'))
