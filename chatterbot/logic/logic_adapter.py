from chatterbot.adapters import Adapter
from chatterbot.utils import import_module


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.

    :param statement_comparison_function: The dot-notated import path
        to a statement comparison function.
        Defaults to ``levenshtein_distance``.

    :param response_selection_method: The a response selection method.
        Defaults to ``get_first_response``.

    :param maximum_similarity_threshold:
        The maximum amount of similarity between two statement that is required
        before the search process is halted. The search for a matching statement
        will continue until a statement with a greater than or equal similarity
        is found or the search set is exhausted.
        Defaults to 0.95

    :param excluded_words:
        The excluded_words parameter allows a list of words to be set that will
        prevent the logic adapter from returning statements that have text
        containing any of those words. This can be useful for preventing your
        chat bot from saying swears when it is being demonstrated in front of
        an audience.
        Defaults to None

    :param search_page_size:
        The maximum number of records to load into memory at a time when searching
        Defaults to 1000
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.comparisons import levenshtein_distance
        from chatterbot.response_selection import get_first_response

        # Import string module parameters
        if 'statement_comparison_function' in kwargs:
            import_path = kwargs.get('statement_comparison_function')
            if isinstance(import_path, str):
                kwargs['statement_comparison_function'] = import_module(import_path)

        if 'response_selection_method' in kwargs:
            import_path = kwargs.get('response_selection_method')
            if isinstance(import_path, str):
                kwargs['response_selection_method'] = import_module(import_path)

        self.maximum_similarity_threshold = kwargs.get(
            'maximum_similarity_threshold', 0.95
        )

        self.excluded_words = kwargs.get('excluded_words')

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

        # By default, compare statements using Levenshtein distance
        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

        # By default, select the first available response
        self.select_response = kwargs.get(
            'response_selection_method',
            get_first_response
        )

    def can_process(self, statement):
        """
        A preliminary check that is called to determine if a
        logic adapter can process a given statement. By default,
        this method returns true but it can be overridden in
        child classes as needed.

        :rtype: bool
        """
        return True

    def process(self, statement):
        """
        Override this method and implement your logic for selecting a response to an input statement.

        A confidence value and the selected response statement should be returned.
        The confidence value represents a rating of how accurate the logic adapter
        expects the selected response to be. Confidence scores are used to select
        the best response from multiple logic adapters.

        The confidence value should be a number between 0 and 1 where 0 is the
        lowest confidence level and 1 is the highest.

        :param statement: An input statement to be processed by the logic adapter.
        :type statement: Statement

        :rtype: Statement
        """
        raise self.AdapterMethodNotImplementedError()

    @property
    def class_name(self):
        """
        Return the name of the current logic adapter class.
        This is typically used for logging and debugging.
        """
        return str(self.__class__.__name__)
