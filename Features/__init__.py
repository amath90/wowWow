import io
from abc import (
    ABCMeta,
    abstractmethod,
)

from cssselect.xpath import GenericTranslator
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class LocatorNotFoundError(Exception):

    def __init__(self, expression, locator, *args, **kwargs):
        self.expression = expression
        self.locator = locator
        super().__init__(*args, **kwargs)


class Locator(metaclass=ABCMeta):

    def __init__(self, expression, parent=None):
        self.expression = expression
        self.parent = parent

    @staticmethod
    @abstractmethod
    def lookup(context, expression):
        pass

    @property
    @abstractmethod
    def BY_EXPR(self):
        pass

    def find(self, context, expression):
        try:
            return self.lookup(context, expression)
        except NoSuchElementException:
            raise LocatorNotFoundError(expression, str(self))

    @staticmethod
    def escape(value):
        if isinstance(value, str):
            return GenericTranslator.xpath_literal(value)
        elif isinstance(value, int):
            return str(value)
        else:
            raise TypeError('Unsupported value type')

    def format_expression(self, params):
        escaped_params = {
            key: self.escape(value)
            for key, value in params.items()
        }
        return self.expression.format(**escaped_params)

    def __call__(self, context, **params):
        if self.parent:
            context = self.parent(context, **params)
        expression = self.format_expression(params)
        return self.find(context, expression)

    def get(self, context, **params):
        try:
            return self(context, **params)
        except LocatorNotFoundError:
            return None

    def get_by_expression(self, **params):
        # Cannot generate a BY expression for nested locators, because
        # they might be different types (for example CSS inside XPath).
        assert not self.parent
        expression = self.format_expression(params)
        return (self.BY_EXPR, expression)

    def __str__(self):
        output = io.StringIO()
        output.write(self.__class__.__name__)
        output.write('(')
        output.write(repr(self.expression))
        output.write(')')
        if self.parent:
            output.write(' within ')
            output.write(str(self.parent))
        return output.getvalue()


class XPath(Locator):

    BY_EXPR = By.XPATH

    @staticmethod
    def lookup(context, expression):
        return context.find_element_by_xpath(expression)


class CSSPath(Locator):

    BY_EXPR = By.CSS_SELECTOR

    @staticmethod
    def lookup(context, expression):
        return context.find_element_by_css_selector(expression)


class MultiXPath(XPath):

    @staticmethod
    def lookup(context, expression):
        return context.find_elements_by_xpath(expression)


class MultiCSSPath(CSSPath):

    @staticmethod
    def lookup(context, expression):
        return context.find_elements_by_css_selector(expression)
