class A:
    def _get_usages_for_locations(
        self,
        param1,
        param2,
        param3,
        param4,
    ):
        """Returns a list of usages for a given location that of the usage type passed in
        Args:
            param1 (str): unique identifier for the API call defined in integration.common.cloud.azure.constants
            param2 (func): function to be passed to extract_list_from_call_results
            param3 (type): type of usage to return (should be one of the types in integration.azure.api.model)
            param4 (list<str>): list of locations to poll for usages

        Return:
            (list<things>): some things to return

        """


def foo(x):
    """
    hi mom!
    Args:
        x (bool): woah
    Return:
        list<str>: non parenthesized return type

    """
