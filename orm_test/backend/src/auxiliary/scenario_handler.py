from copy import deepcopy

class ScenarioHandler:
    """
    A class for handling scenarios, represented by dictionaries. 
    The class provides methods for obtaining a relevant part of a scenario,
    checking if the keys are properly filled, merging two dictionaries,
    checking if a key chain is in the dictionary, and adding values to a
    dictionary.
    """
    def __init__(self, scenario_dict: dict):
        """
        Initialize the ScenarioHandler with the given scenario dictionary.

        Args:
            scenario_dict (dict): The scenario dictionary to be handled.
        """
        self.scenario_dict = scenario_dict
    
    def getRelevantScenarioDict(self, relevant_scenario_keys: list) -> dict:
        """
        Get a part of the scenario dictionary that is relevant based on the
        provided keys.

        Args:
            relevant_scenario_keys (list): The keys that determine which part
            of the scenario dictionary is relevant.

        Returns:
            dict: The part of the scenario dictionary that is relevant.
        """
        self.__checkIfRelevantScenarioKeysIsFilled(relevant_scenario_keys)

        relevant_scenarios = {}
        for key_chain in relevant_scenario_keys:
            if not self.__isKeyChainInDict(self.scenario_dict, key_chain):
                continue

            key_chain_list = list(key_chain)
            to_add_dict = self.__addValuesToDict(
                key_chain_list,
                self.scenario_dict,
                {}
            )
            relevant_scenarios = self.__mergeTwoDicts(
                relevant_scenarios,
                to_add_dict
            )
        return relevant_scenarios

    @staticmethod
    def __checkIfRelevantScenarioKeysIsFilled(
        relevant_scenario_keys: list
    ) -> None:
        """
        Check if the relevant_scenario_keys are properly set.

        Raises:
            TypeError: If the relevant_scenario_keys list is not of type list
                or contains not only tuples.
        """
        if type(relevant_scenario_keys) != list:
            raise TypeError(
                f'''
                The attribute "relevant_scenario_keys" needs to be of type list
                not {type(relevant_scenario_keys)}.
                '''
            )

        for scenario_key in relevant_scenario_keys:
            if type(scenario_key) != tuple:
                raise TypeError(
                    f'''
                    Each entry in relevant_scenario_keys needs to be of type
                    tuple not {type(scenario_key)}. 
                    (E.g. relevant_scenario_keys= [
                        ('volume', 'project'),
                        ('derivative',)
                    ] not {scenario_key})
                    '''
                )

    @staticmethod
    def __mergeTwoDicts(
        dict_1: dict,
        dict_2: dict,
        path: None | list = None
    ) -> dict:
        """
        Merge two dictionaries.

        Args:
            dict_1 (dict): The first dictionary.
            dict_2 (dict): The second dictionary.
            path (None | list, optional): A path in the dictionaries.
                Defaults to None.

        Returns:
            dict: The merged dictionary.
        
        Raises:
            Exception: If there is a conflict between the dictionaries.
        """
        output_dict = deepcopy(dict_1)
        if path is None: path = []
        for key in dict_2:
            if key in output_dict:
                if (
                    isinstance(output_dict[key], dict) and
                    isinstance(dict_2[key], dict)
                ):
                    ScenarioHandler.__mergeTwoDicts(
                        output_dict[key],
                        dict_2[key],
                        path + [key]
                    )
                elif output_dict[key] == dict_2[key]:
                    pass # same leaf value
                else:
                    raise Exception(f'Conflict at {key}')
            else:
                output_dict[key] = dict_2[key]
        return output_dict

    @staticmethod
    def __isKeyChainInDict(to_check_dict: dict, key_chain: tuple) -> bool:
        """
        Check if a key chain is in a dictionary.

        Args:
            to_check_dict (dict): The dictionary to check.
            key_chain (tuple): The key chain to check for.

        Returns:
            bool: True if the key chain is in the dictionary, False otherwise.
        """
        if len(key_chain) == 0:
            return True
        if (type(to_check_dict) != dict or
            key_chain[0] not in to_check_dict.keys()
        ):
            return False
        return ScenarioHandler.__isKeyChainInDict(
            to_check_dict[key_chain[0]],
            key_chain[1:]
        )

    @staticmethod
    def __addValuesToDict(
        key_chain: list,
        to_add_dict: dict,
    ) -> dict:
        """
        Add values to a dictionary based on a key chain.

        Args:
            key_chain (list): The key chain determining which values to add.
            to_add_dict (dict): The dictionary from which to get the values.

        Returns:
            dict: The output dictionary with added values.
        """
        output_dict = None

        if output_dict is None:
            output_dict = {}

        if len(key_chain) == 0:
            return to_add_dict

        key = key_chain.pop(0)
        output_dict[key] = ScenarioHandler.__addValuesToDict(key_chain, to_add_dict[key])

        return output_dict
