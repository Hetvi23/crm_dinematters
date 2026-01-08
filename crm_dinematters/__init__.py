# This is a wrapper package for bench compatibility
# The actual app module is 'crm'
from crm import *

# Expose version for bench
__version__ = getattr(__import__('crm'), '__version__', '1.57.2')
__title__ = getattr(__import__('crm'), '__title__', 'Frappe CRM')
