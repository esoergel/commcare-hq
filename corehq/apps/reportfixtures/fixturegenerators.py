import logging
from xml.etree import ElementTree
from casexml.apps.case.xml import V2
from corehq.apps.domain.models import Domain
from corehq.apps.callcenter.indicator_sets import CallCenter
from corehq.apps.users.models import CommCareUser


logger = logging.getLogger(__name__)


def indicators(user, version=V2, last_sync=None):
    if isinstance(user, CommCareUser):
        pass
    elif hasattr(user, "_hq_user") and user._hq_user is not None:
        user = user._hq_user
    else:
        return []

    fixtures = []
    indicator_sets = []
    for dom in user.get_domains():
        domain = Domain.get_by_name(dom)
        if hasattr(domain, 'call_center_config') and domain.call_center_config.enabled:
            indicator_sets.append(CallCenter(domain, user))

    for set in indicator_sets:
        try:
            fixtures.append(gen_fixture(user, set))
        except Exception as e:  # blanket exception catching intended
            logger.exception('problem generating report fixtures for user {user}: {msg}'.format(
                user=user._id, msg=str(e)))

    return fixtures


def gen_fixture(user, indicator_set):
    """
    Generate the fixture from the indicator data.

    :param user: The user.
    :param indicator_set: A subclass of SqlIndicatorSet
    :param include_empty: True to include indicators that have no value for the current time period.
    """
    """
    Example output:
    indicator_set {
        name = 'demo'
        group = None
        data = {'indicator_a': 1}
    }
    <fixture id="indicators:demo" user_id="...">
        <indicators>
            <indicator_a>1</indicator_a>
            <indicator_b>0</indicator_b>
        </indicators>
    </fixture>

    indicator_set {
        name = 'demo'
        group = 'user'
        data = {'user1': {'user': 'user1', 'indicator_a': 1}}
    }
    <fixture id="indicators:demo" user_id="...">
        <indicators>
            <user id="user1">
                <indicator_a>1</indicator_a>
            </user>
        </indicators>
    </fixture>
    """
    name = indicator_set.name
    group = indicator_set.group_by
    data = indicator_set.data

    xFixture = ElementTree.Element('fixture', attrib={'id': 'indicators:%s' % name, 'user_id': user.user_id})
    xIndicators = ElementTree.SubElement(xFixture, 'indicators')
    if group:
        if len(group) > 1:
            raise Exception("Only single level grouping supported.")

        group_name = group[0]
        group_columns = [c for c in indicator_set.columns if c.view.name == group_name]
        for group_id, group_data in data.items():
            elem_name = group_columns[0].header if group_columns else group_name
            xGroup = ElementTree.SubElement(xIndicators, elem_name, attrib={'id': group_id})
            for c in indicator_set.columns:
                key = c.view.name
                if key != group_name:
                    xIndicator = ElementTree.SubElement(xGroup, c.header)
                    xIndicator.text = str(group_data.get(key, 0))
    elif data:
        for c in indicator_set.columns:
            key = c.view.name
            xIndicator = ElementTree.SubElement(xIndicators, c.header)
            xIndicator.text = str(data.get(key, 0))

    return xFixture
