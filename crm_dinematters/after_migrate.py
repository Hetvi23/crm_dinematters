# This module provides after_migrate hooks for crm_dinematters
# It wraps the original crm hooks and adds default lead statuses

import frappe


def after_migrate():
	"""After migrate hook that safely handles app name mismatch"""
	try:
		# Add default lead statuses (skipped during after_install due to controller loading issues)
		from crm.install import add_default_lead_statuses
		add_default_lead_statuses()
		
		# Call the original after_migrate hook for FCRM Settings dropdown items
		from crm.fcrm.doctype.fcrm_settings.fcrm_settings import after_migrate as _fcrm_after_migrate
		_fcrm_after_migrate()
	except Exception as e:
		# Log error but don't fail migration
		frappe.log_error(
			title="After Migrate Error",
			message=f"Error in after_migrate hook: {str(e)}"
		)
