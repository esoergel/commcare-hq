from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_noop
from corehq.apps.appstore.views import fill_mapping_with_facets
from corehq.apps.reports.datatables import DataTablesHeader, DataTablesColumn, DTSortType
from corehq.apps.reports.dispatcher import BasicReportDispatcher, AdminReportDispatcher
from corehq.apps.reports.generic import GenericTabularReport, ElasticTabularReport
from django.utils.translation import ugettext as _
from corehq.pillows.mappings.domain_mapping import DOMAIN_INDEX

def format_date(dstr, default):
    return datetime.strptime(dstr, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y/%m/%d %H:%M:%S') if dstr else default

class DomainStatsReport(GenericTabularReport):
    dispatcher = BasicReportDispatcher
    asynchronous = True
    section_name = 'DOMSTATS'
    base_template = "reports/async/default.html"
    custom_params = []
    es_queried = False

    name = ugettext_noop('Domain Statistics')
    slug = 'dom_stats'

    def get_domains(self):
        return getattr(self, 'domains', [])

    def is_custom_param(self, param):
        raise NotImplementedError

    def get_name_or_link(self, d, internal_settings=False):
        if not getattr(self, 'show_name', None):
            reverse_str = "domain_homepage" if not internal_settings else "domain_internal_settings"
            return mark_safe('<a href="%s">%s</a>' % \
                   (reverse(reverse_str, args=[d['name']]), d.get('hr_name') or d['name']))
        else:
            return d['name']

    @property
    def es_results(self):
        if not getattr(self, 'es_response', None):
            self.es_query()
        return self.es_response

    def es_query(self):
        if not self.es_queried:
            results = es_domain_query(domains=[d.name for d in self.get_domains()])
            self.es_queried = True
            self.es_response = results
        return self.es_response

    @property
    def headers(self):
        headers = DataTablesHeader(
            DataTablesColumn("Project", prop_name="name.exact"),
            DataTablesColumn(_("# Active Mobile Workers"), sort_type=DTSortType.NUMERIC,
                prop_name="cp_n_active_cc_users",
                help_text=_("The number of mobile workers who have submitted a form in the last 30 days")),
            DataTablesColumn(_("# Mobile Workers"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_cc_users"),
            DataTablesColumn(_("# Active Cases"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_active_cases",
                help_text=_("The number of cases modified in the last 120 days")),
            DataTablesColumn(_("# Cases"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_cases"),
            DataTablesColumn(_("# Form Submissions"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_forms"),
            DataTablesColumn(_("First Form Submission"), prop_name="cp_first_form"),
            DataTablesColumn(_("Last Form Submission"), prop_name="cp_last_form"),
            DataTablesColumn(_("# Web Users"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_web_users"),
        )
        return headers

    @property
    def rows(self):
        domains = [res['_source'] for res in self.es_results.get('hits', {}).get('hits', [])]

        for dom in domains:
            if dom.has_key('name'): # for some reason when using the statistical facet, ES adds an empty dict to hits
                yield [
                    self.get_name_or_link(dom),
                    dom.get("cp_n_active_cc_users", _("Not yet calculated")),
                    dom.get("cp_n_cc_users", _("Not yet calculated")),
                    dom.get("cp_n_active_cases", _("Not yet calculated")),
                    dom.get("cp_n_cases", _("Not yet calculated")),
                    dom.get("cp_n_forms", _("Not yet calculated")),
                    format_date(dom.get("cp_first_form"), _("No forms")),
                    format_date(dom.get("cp_last_form"), _("No forms")),
                    dom.get("cp_n_web_users", _("Not yet calculated"))
                ]

    @property
    def shared_pagination_GET_params(self):
        ret = super(DomainStatsReport, self).shared_pagination_GET_params
        for param in self.request.GET.iterlists():
            if self.is_custom_param(param[0]):
                for val in param[1]:
                    ret.append(dict(name=param[0], value=val))
        return ret

class OrgDomainStatsReport(DomainStatsReport):
    override_permissions_check = True

    def get_domains(self):
        from corehq.apps.orgs.models import Organization
        from corehq.apps.domain.models import Domain
        org = self.request.GET.get('org', None)
        organization = Organization.get_by_name(org, strict=True)
        if organization and \
                (self.request.couch_user.is_superuser or self.request.couch_user.is_member_of_org(org)):
            return [d for d in Domain.get_by_organization(organization.name).all()]
        return []

    def is_custom_param(self, param):
        return param in ['org']

DOMAIN_FACETS = [
    "cp_is_active",
    "cp_has_app",
    "uses reminders",
    "project_type",
    "area",
    "case_sharing",
    "commtrack_enabled",
    "customer_type",
    "deployment.city.exact",
    "deployment.country.exact",
    "deployment.date",
    "deployment.public",
    "deployment.region.exact",
    "hr_name",
    "internal.area.exact",
    "internal.can_use_data",
    "internal.commcare_edition",
    "internal.custom_eula",
    "internal.initiative.exact",
    "internal.project_state",
    "internal.self_started",
    "internal.services",
    "internal.sf_account_id",
    "internal.sf_contract_id",
    "internal.sub_area.exact",
    "internal.using_adm",
    "internal.using_call_center",
    "internal.platform",

    "is_approved",
    "is_public",
    "is_shared",
    "is_sms_billable",
    "is_snapshot",
    "is_test",
    "license",
    "multimedia_included",

    "phone_model",
    "published",
    "sub_area",
    "survey_management_enabled",
    "tags",
]

FACET_MAPPING = [
    ("Activity", True, [
        {"facet": "is_test", "name": "Test Project", "expanded": True },
        {"facet": "cp_is_active", "name": "Active", "expanded": True },
        # {"facet": "deployment.date", "name": "Deployment Date", "expanded": False },
        {"facet": "internal.project_state", "name": "Scale", "expanded": False },
    ]),
    ("Location", True, [
        {"facet": "deployment.country.exact", "name": "Country", "expanded": True },
        {"facet": "deployment.region.exact", "name": "Region", "expanded": False },
        {"facet": "deployment.city.exact", "name": "City", "expanded": False },
    ]),
    ("Type", True, [
        {"facet": "internal.area.exact", "name": "Area", "expanded": True },
        {"facet": "internal.sub_area.exact", "name": "Sub Area", "expanded": True },
        {"facet": "phone_model", "name": "Phone Model", "expanded": False },
    ]),
    ("Self Starters", False, [
        {"facet": "internal.self_started", "name": "Self Started", "expanded": True },
        {"facet": "cp_has_app", "name": "Has App", "expanded": False },
    ]),
    ("Advanced Features", False, [
        # {"facet": "", "name": "Reminders", "expanded": True },
        {"facet": "case_sharing", "name": "Case Sharing", "expanded": False },
        {"facet": "internal.using_adm", "name": "ADM", "expanded": False },
        {"facet": "internal.using_call_center", "name": "Call Center", "expanded": False },
        {"facet": "commtrack_enabled", "name": "CommTrack", "expanded": False },
        {"facet": "survey_management_enabled", "name": "Survey Management", "expanded": False },
    ]),
    ("Plans", False, [
        {"facet": "project_type", "name": "Project Type", "expanded": False },
        {"facet": "customer_type", "name": "Customer Type", "expanded": False },
        {"facet": "internal.initiative.exact", "name": "Initiative", "expanded": False },
        {"facet": "internal.commcare_edition", "name": "CommCare Pricing Edition", "expanded": False },
        {"facet": "internal.services", "name": "Services", "expanded": False },
        {"facet": "is_sms_billable", "name": "SMS Billable", "expanded": False },
    ]),
    ("Eula", False, [
        {"facet": "internal.can_use_data", "name": "Public Data", "expanded": True },
        {"facet": "custom_eula", "name": "Custom Eula", "expanded": False },
    ]),
]

def es_domain_query(params=None, facets=None, terms=None, domains=None, return_q_dict=False, start_at=None, size=None, sort=None):
    from corehq.apps.appstore.views import es_query
    if params is None:
        params = {}
    if terms is None:
        terms = ['search']
    if facets is None:
        facets = []
    q = {"query": {"match_all":{}}}

    if domains is not None:
        q["query"] = {
            "in" : {
                "name" : domains,
            }
        }

    q["filter"] = {"and": [
        {"term": {"doc_type": "Domain"}},
        {"term": {"is_snapshot": False}},
    ]}

    search_query = params.get('search', "")
    if search_query:
        q['query'] = {
            "bool": {
                "must": {
                    "match" : {
                        "_all" : {
                            "query" : search_query,
                            "operator" : "or", }}}}}

    q["facets"] = {}
    stats = ['cp_n_active_cases', 'cp_n_inactive_cases', 'cp_n_active_cc_users', 'cp_n_cc_users', 'cp_n_60_day_cases', 'cp_n_web_users', 'cp_n_forms', 'cp_n_cases']
    for prop in stats:
        q["facets"].update({"%s-STATS" % prop: {"statistical": {"field": prop}}})

    q["sort"] = sort if sort else [{"name" : {"order": "asc"}},]

    return es_query(params, facets, terms, q, DOMAIN_INDEX + '/hqdomain/_search', start_at, size, dict_only=return_q_dict)

ES_PREFIX = "es_"
class AdminDomainStatsReport(DomainStatsReport, ElasticTabularReport):
    default_sort = None
    slug = "domains"
    dispatcher = AdminReportDispatcher
    base_template = "hqadmin/stats_report.html"
    asynchronous = False
    ajax_pagination = True
    exportable = True

    @property
    def template_context(self):
        ctxt = super(AdminDomainStatsReport, self).template_context

        self.es_query()

        ctxt.update({
            'layout_flush_content': True,
            'facet_map': self.es_facet_mapping,
            'query_str': self.request.META['QUERY_STRING'],
            'facet_prefix': ES_PREFIX,
            'grouped_facets': True,
        })
        return ctxt

    @property
    def total_records(self):
        return int(self.es_results['hits']['total'])

    def es_query(self):
        from corehq.apps.appstore.views import parse_args_for_es, generate_sortables_from_facets
        if not self.es_queried:
            self.es_params, _ = parse_args_for_es(self.request, prefix=ES_PREFIX)
            self.es_facets = DOMAIN_FACETS
            results = es_domain_query(self.es_params, self.es_facets, sort=self.get_sorting_block(),
                start_at=self.pagination.start, size=self.pagination.count)
            self.es_facet_mapping = fill_mapping_with_facets(FACET_MAPPING, results, self.es_params)
            self.es_queried = True
            self.es_response = results
        return self.es_response

    def is_custom_param(self, param):
        return param.startswith(ES_PREFIX)

    @property
    def headers(self):
        headers = DataTablesHeader(
            DataTablesColumn("Project", prop_name="name.exact"),
            DataTablesColumn(_("Organization"), prop_name="internal.organization_name"),
            DataTablesColumn(_("Deployment Date"), prop_name="deployment.date"),
            DataTablesColumn(_("Deployment Country"), prop_name="deployment.country.exact"),
            DataTablesColumn(_("# Active Mobile Workers"), sort_type=DTSortType.NUMERIC,
                prop_name="cp_n_active_cc_users",
                help_text=_("The number of mobile workers who have submitted a form in the last 30 days")),
            DataTablesColumn(_("# Mobile Workers"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_cc_users"),
            DataTablesColumn(_("# Cases in last 60"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_60_day_cases",
                help_text=_("The number of cases modified in the last 60 days")),
            DataTablesColumn(_("# Active Cases"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_active_cases",
                help_text=_("The number of cases modified in the last 120 days")),
            DataTablesColumn(_("# Inactive Cases"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_inactive_cases",
                help_text=_("The number of open cases not modified in the last 120 days")),
            DataTablesColumn(_("# Cases"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_cases"),
            DataTablesColumn(_("# Form Submissions"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_forms"),
            DataTablesColumn(_("First Form Submission"), prop_name="cp_first_form"),
            DataTablesColumn(_("Last Form Submission"), prop_name="cp_last_form"),
            DataTablesColumn(_("# Web Users"), sort_type=DTSortType.NUMERIC, prop_name="cp_n_web_users"),
            DataTablesColumn(_("Notes"), prop_name="internal.notes"),
            DataTablesColumn(_("Services"), prop_name="internal.services"),
            DataTablesColumn(_("Project State"), prop_name="internal.project_state"),
            DataTablesColumn(_("Using ADM?"), prop_name="internal.using_adm"),
            DataTablesColumn(_("Using Call Center?"), prop_name="internal.using_call_center"),
        )
        return headers

    @property
    def export_table(self):
        self.pagination.count = 1000000 # terrible hack to get the export to return all rows
        self.show_name = True
        return super(AdminDomainStatsReport, self).export_table


    @property
    def rows(self):
        domains = [res['_source'] for res in self.es_results.get('hits', {}).get('hits', [])]

        def get_from_stat_facets(prop, what_to_get):
            return self.es_results.get('facets', {}).get('%s-STATS' % prop, {}).get(what_to_get)

        CALCS_ROW_INDEX = {
            4: "cp_n_active_cc_users",
            5: "cp_n_cc_users",
            6: "cp_n_60_day_cases",
            7: "cp_n_active_cases",
            8: "cp_n_inactive_cases",
            9: "cp_n_cases",
            10: "cp_n_forms",
            13: "cp_n_web_users",
        }
        def stat_row(name, what_to_get, type='float'):
            row = [name]
            for index in range(1, len(self.headers)):
                if index in CALCS_ROW_INDEX:
                    val = get_from_stat_facets(CALCS_ROW_INDEX[index], what_to_get)
                    row.append('%.2f' % float(val) if val and type=='float' else val or "Not yet calculated")
                else:
                    row.append('---')
            return row

        self.total_row = stat_row(_('Total'), 'total', type='int')
        self.statistics_rows = [
            stat_row(_('Mean'), 'mean'),
            stat_row(_('STD'), 'std_deviation'),
        ]

        def format_date(dstr, default):
            # use [:19] so that only only the 'YYYY-MM-DDTHH:MM:SS' part of the string is parsed
            return datetime.strptime(dstr[:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y/%m/%d %H:%M:%S') if dstr else default

        def get_name_or_link(d):
            if not getattr(self, 'show_name', None):
                return mark_safe('<a href="%s">%s</a>' % \
                       (reverse("domain_homepage", args=[d['name']]), d.get('hr_name') or d['name']))
            else:
                return d['name']

        for dom in domains:
            if dom.has_key('name'): # for some reason when using the statistical facet, ES adds an empty dict to hits
                yield [
                    self.get_name_or_link(dom, internal_settings=True),
                    dom.get("internal", {}).get('organization_name') or _('No org'),
                    format_date(dom.get('deployment', {}).get('date'), _('No date')),
                    dom.get("deployment", {}).get('country') or _('No country'),
                    dom.get("cp_n_active_cc_users", _("Not yet calculated")),
                    dom.get("cp_n_cc_users", _("Not yet calculated")),
                    dom.get("cp_n_60_day_cases", _("Not yet calculated")),
                    dom.get("cp_n_active_cases", _("Not yet calculated")),
                    dom.get("cp_n_inactive_cases", _("Not yet calculated")),
                    dom.get("cp_n_cases", _("Not yet calculated")),
                    dom.get("cp_n_forms", _("Not yet calculated")),
                    format_date(dom.get("cp_first_form"), _("No forms")),
                    format_date(dom.get("cp_last_form"), _("No forms")),
                    dom.get("cp_n_web_users", _("Not yet calculated")),
                    dom.get('internal', {}).get('notes') or _('No notes'),
                    dom.get('internal', {}).get('services') or _('No info'),
                    dom.get('internal', {}).get('project_state') or _('No info'),
                    dom.get('internal', {}).get('using_adm') or False,
                    dom.get('internal', {}).get('using_call_center') or False,
                ]
