# Request Context and Scope Resolution

class RequestContext:
    """
    Manages request context including scope resolution for centres and dates.
    """
    
    def __init__(self):
        self.scope = None  # centre, selected, all
        self.centre_names = []  # List of centre names for 'selected' scope
        self.centre_name = None  # Single centre name for 'centre' scope
        self.date_scope = None  # single, range, latest, all, batch
        self.date = None  # Single date for 'single' date_scope
        self.from_date = None  # Start date for 'range' date_scope
        self.to_date = None  # End date for 'range' date_scope
        self.dates = []  # List of dates for 'batch' date_scope
        self.filters = {}  # Optional user-controlled filters
        self.metric = None  # farmers, quantity, amount
        self.include_summary = True
        self.force_refresh = False
        self.sync_if_missing = True
    
    def resolve_scope(self):
        """
        Resolves the effective scope based on provided parameters.
        Returns a tuple of (scope_type, scope_values).
        """
        if self.scope == 'centre' and self.centre_name:
            return ('centre', [self.centre_name])
        elif self.scope == 'selected' and self.centre_names:
            return ('selected', self.centre_names)
        elif self.scope == 'all':
            return ('all', [])
        else:
            # Default to all if no valid scope specified
            return ('all', [])
    
    def resolve_date_scope(self):
        """
        Resolves the effective date scope based on provided parameters.
        Returns a tuple of (date_scope_type, date_values).
        """
        if self.date_scope == 'single' and self.date:
            return ('single', [self.date])
        elif self.date_scope == 'range' and self.from_date and self.to_date:
            return ('range', [self.from_date, self.to_date])
        elif self.date_scope == 'latest':
            return ('latest', [])
        elif self.date_scope == 'all':
            return ('all', [])
        elif self.date_scope == 'batch' and self.dates:
            return ('batch', self.dates)
        else:
            # Default to all if no valid date scope specified
            return ('all', [])