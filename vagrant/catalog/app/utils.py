from flask import flash
from wtforms import SelectMultipleField
from slugify import Slugify
# Misc utils methods


def flash_errors(form):
    # Taken from http://flask.pocoo.org/snippets/12/
    form_errors = getattr(form, 'errors', {'items': []})
    for field, errors in form_errors.items():
        for error in errors:
            flash(u"Error in %s - %s" % (
                getattr(form, field).label.text,
                error
            ))


def slugify_category_list(category_list):
    if category_list is not None:
        slugifier = Slugify(to_lower=True)
        slugified_list = []
        for cat in category_list:
            cat_elem = cat.split('|')
            if len(cat_elem) == 1:
                cat_elem.append(cat_elem[0])
            slugified_list.append([cat, cat_elem[0], slugifier(cat_elem[1])])
        return slugified_list


class OpenSelectMultipleField(SelectMultipleField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """
    # Taken from http://stackoverflow.com/a/31282492/2423859
    def pre_validate(self, form):
        pass

    # def process_formdata(self, valuelist):
    #     # slugify the categories from the form
    #     slugifier = Slugify(to_lower=True)
    #     try:
    #
    #         self.data = list(slugifier(self.coerce(x)) for x in valuelist)
    #     except ValueError:
    #         raise ValueError(self.gettext('Invalid choice(s): one or more ' +
    #                                     ' data inputs could not be coerced'))
