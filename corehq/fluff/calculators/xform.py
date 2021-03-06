from datetime import timedelta
from corehq.fluff.calculators.logic import ANDCalculator, ORCalculator
import fluff

def default_date(form):
    return form.received_on

# operators
EQUAL = lambda input, reference: input == reference
NOT_EQUAL = lambda input, reference: input != reference
IN = lambda input, reference_list: input in reference_list
IN_MULTISELECT = lambda input, reference: reference in (input or '').split(' ')
ANY = lambda input, reference: bool(input)

def ANY_IN_MULTISELECT(input, reference):
    """
    For 'this multiselect contains any one of these N items'
    """
    return any([subval in (input or '').split(' ') for subval in reference])


class IntegerPropertyReference(object):
    """
    Returns the integer value of the property_path passed in.

    By default FilteredFormPropertyCalculator would use 1 for all results
    but this will let you return the actual number to be summed.

    Accepts an optional transform lambda/method that would modify the
    resulting integer before returning it.
    """
    def __init__(self, property_path, transform=None):
        self.property_path = property_path
        self.transform = transform

    def __call__(self, form):
        value = int(form.xpath(self.property_path) or 0)
        if value and self.transform:
            value = self.transform(value)
        return value

class FilteredFormPropertyCalculator(fluff.Calculator):
    """
    Enables filtering forms by xmlns and (optionally) property == value.
    Let's you easily define indicators such as:
     - all adult registration forms
     - all child registration forms with foo.bar == baz
     - all newborn followups with bippity != bop

    By default just emits a single "total" value for anything matching the filter,
    though additional fields can be added by subclassing.

    These can also be chained using logic operators for fun and profit.
    """

    xmlns = None
    property_path = None
    property_value = None
    indicator_calculator = None
    window = timedelta(days=1)

    @fluff.date_emitter
    def total(self, form):
        if self.indicator_calculator:
            yield default_date(form)
        else:
            yield [default_date(form), self.indicator_calculator(form)]

    def __init__(self, xmlns=None, property_path=None, property_value=None,
                 operator=EQUAL, indicator_calculator=None, window=None):
        def _conditional_setattr(key, value):
            if value:
                setattr(self, key, value)

        _conditional_setattr('xmlns', xmlns)
        assert self.xmlns is not None

        _conditional_setattr('property_path', property_path)
        _conditional_setattr('property_value', property_value)
        if self.property_path is not None and operator != ANY:
            assert self.property_value is not None

        self.operator = operator
        _conditional_setattr('indicator_calculator', indicator_calculator)

        super(FilteredFormPropertyCalculator, self).__init__(window)

    def filter(self, form):
        # filter
        return (
            form.xmlns == self.xmlns and (
                self.property_path is None or
                self.operator(form.xpath(self.property_path), self.property_value)
            )
        )


# meh this is a little redundant but convenient
class FormANDCalculator(ANDCalculator):
    window = timedelta(days=1)

    @fluff.date_emitter
    def total(self, form):
        yield default_date(form)

class FormORCalculator(ORCalculator):
    window = timedelta(days=1)

    @fluff.date_emitter
    def total(self, form):
        yield default_date(form)

class FormSUMCalculator(ORCalculator):
    window = timedelta(days=1)

    @fluff.date_emitter
    def total(self, form):
        for calc in self.calculators:
            if calc.passes_filter(form):
                for total in calc.total(form):
                    yield total
