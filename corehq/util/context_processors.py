from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import Http404

RAVEN = bool(getattr(settings, 'SENTRY_DSN', None))

def base_template(request):
    """This sticks the base_template variable defined in the settings
       into the request context."""

    return {
        'base_template': settings.BASE_TEMPLATE,
        'login_template': settings.LOGIN_TEMPLATE,
    }


def get_per_domain_context(project):
    if project and project.commtrack_enabled:
        domain_type = 'commtrack'
        logo = 'hqstyle/img/commtrack-logo.png'
        site_name = "CommTrack"
        public_site = "http://www.commtrack.org"
        can_be_your = "mobile logistics solution"
    else:
        domain_type = 'commcare'
        logo = 'hqstyle/img/commcare-logo.png'
        site_name = "CommCare HQ"
        public_site = "http://www.commcarehq.org"
        can_be_your = "mobile health solution"

    return {
        'DOMAIN_TYPE': domain_type,
        'LOGO': logo,
        'SITE_NAME': site_name,
        'CAN_BE_YOUR': can_be_your,
        'PUBLIC_SITE': public_site,
    }


def domain(request):
    """Global per-domain context variables"""

    project = getattr(request, 'project', None)
    return get_per_domain_context(project)


def current_url_name(request):
    """
    Adds the name for the matched url pattern for the current request to the
    request context.
    
    """
    try:
        match = resolve(request.path)
        url_name = match.url_name
    except Http404:
        url_name = None
    
    return {
        'current_url_name': url_name
    }


def analytics_js(request):
    return settings.ANALYTICS_IDS

def raven(request):
    """lets you know whether raven is being used"""
    return {
        'RAVEN': RAVEN
    }
