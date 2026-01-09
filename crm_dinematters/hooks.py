# This is a wrapper hooks file for bench compatibility
# The actual hooks are in 'crm.hooks'
# Import everything from crm.hooks to make it available as crm_dinematters.hooks
from crm.hooks import *

# Override app_name to match the installed app name (crm_dinematters)
# This is necessary for bench to correctly identify the app during installation
app_name = "crm_dinematters"

# Override scheduler_events to filter out methods that reference 'crm' app
# Since the app is installed as 'crm_dinematters', Frappe validates scheduler
# methods by checking if the app (first part of module path) is installed.
# The background_sync methods reference 'crm.lead_syncing.*' which fails validation
# because app 'crm' is not installed (only 'crm_dinematters' is).
# We exclude these since they're already handled by crm_essenceerp's scheduler.
scheduler_events = {
	# Empty - background sync is handled by crm_essenceerp's scheduler
}

# Override after_migrate - remove it since it references 'crm' app which isn't installed
# The function syncs FCRM Settings dropdown items, which is optional.
# If needed, it can be run manually via the FCRM Settings doctype.
after_migrate = []
