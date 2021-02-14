#!/usr/bin/python3
from copy import deepcopy

from simple_tools.money import *


class Account:
    """Represent an account of money."""
    __holdings: float  # balance of this account
    __lower_bound: Union[float, None]  # lowest permitted balance
    __upper_bound: Union[float, None]  # highest balance permitted/recommended
    __has_upper_bound: bool  # a lower_bound is in place
    __has_lower_bound: bool  # an upper_bound is in place

    __transfer_to: callable  # transfer holdings from here to elsewhere
    __transfer_from: callable  # transfer holdings from elsewhere to here
    __withdraw: callable  # take from balance
    __deposit: callable  # add to balance

    __override: callable  # correct balance to something given
    __retrieve: callable  # retrieve the balance
    __update: callable  # correct balance to something externally sourced

    __id: int  # identify this account

    _caller_0: callable = lambda fxn, its_id: 0 if fxn is None else fxn(its_id)
    _caller_1: callable = lambda fxn, its_id, argument: True if fxn is None else fxn(its_id, argument)
    _caller_3: callable = lambda fxn, its_id, that_id, argument: True if fxn is None else fxn(its_id, that_id, argument)

    def __init__(self, balance: float, lower_bound: float = None, upper_bound: float = None):
        """
        This class represents a generic financial account.
        :param balance: initial balance
        :param lower_bound: float bottom threshold (None if not applicable)
        :param upper_bound: float top cap (None if not applicable)
        """
        assert (True if lower_bound is None else (True if upper_bound is None else (lower_bound < upper_bound))), "The lower_bound should be below the upper_bound."
        assert ((balance >= lower_bound) if lower_bound is not None else ((balance <= upper_bound) if upper_bound is not None else (lower_bound <= balance <= upper_bound))), "The initial balance should be within the bounds set or not set by the lower_bound and upper_bound."
        self.__holdings = balance
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__has_lower_bound = lower_bound is not None
        self.__has_upper_bound = upper_bound is not None
        self.__id = IdSmuggler.MONEY_ACCOUNT_IDS.next_id()

    # Limits

    def set_upper_bound(self, upper_bound: float = None) -> bool:
        """
        Set a cap on the balance of an account.
        Some accounts IRL do have caps.
        :param upper_bound: float cap (or no cap if None)
        :return: successfully set or not
        """
        if upper_bound is None:
            self.__upper_bound = None
            self.__has_upper_bound = False
        else:
            if self.__holdings <= upper_bound:
                self.__upper_bound = upper_bound
                self.__has_upper_bound = True
            else:
                return False
        return True

    def set_lower_bound(self, lower_bound: float = None) -> bool:
        """
        Set a minimum balance for this account.
        This helps avoid fees and illegality.
        :param lower_bound: float minimum (or no minimum balance if None)
        :return: successfully set or not
        """
        if lower_bound is None:
            self.__lower_bound = None
            self.__has_lower_bound = False
        else:
            if self.__holdings >= lower_bound:
                self.__lower_bound = lower_bound
                self.__has_lower_bound = True
            else:
                return False
        return True

    def has_upper_bound(self) -> bool:
        """
        Indicate whether this account has a cap or not.
        :return: bool
        """
        return self.__has_upper_bound

    def has_lower_bound(self) -> bool:
        """
        Indicate whether this account has a minimum balance or not.
        :return: bool
        """
        return self.__has_lower_bound

    def get_upper_bound(self) -> float:
        """
        If this account has a cap, return it.
        :return: float cap
        """
        return self.__upper_bound

    def get_lower_bound(self) -> float:
        """
        If this account has a minimum balance, return it.
        :return: float minimum balance
        """
        return self.__lower_bound

    # Out-linking

    def get_retrieve_function(self) -> callable:
        """
        Return the fxn the can be called to update the balance.
        :return: callable fxn
        """
        return self.__retrieve

    def get_override_function(self) -> callable:
        """
        Return the fxn that can be called to set the balance.
        :return: callable fxn
        """
        return self.__override

    def get_deposit_function(self) -> callable:
        """
        Return the fxn that can be called to make a deposit into this account.
        :return: callable fxn
        """
        return self.__deposit

    def get_withdraw_function(self) -> callable:
        """
        Return the fxn that can be called to make a withdrawal from this account.
        :return: callable fxn
        """
        return self.__withdraw

    def set_retrieve_function(self, fxn: callable):
        """
        Set the fxn the can be called to update the balance.
        :param fxn: callable fxn
        """
        self.__retrieve = fxn
        return

    def set_override_function(self, fxn: callable):
        """
        Set the fxn that can be called to set the balance.
        :param fxn: callable fxn
        """
        self.__override = fxn
        return

    def set_deposit_function(self, fxn: callable):
        """
        Set the fxn that can be called to make a deposit into this account.
        :param fxn: callable fxn
        """
        self.__deposit = fxn
        return

    def set_withdraw_function(self, fxn: callable):
        """
        Set the fxn that can be called to make a withdrawal from this account.
        :param fxn: callable fxn
        """
        self.__withdraw = fxn
        return

    # More out-linking

    def update_assertive(self) -> bool:
        """
        Update (synchronize) the balance of this account.
        :return: successfully updated or not
        """
        return self.set_balance(self.update_passive())

    def update_passive(self) -> float:
        """
        Retrieve the actual balance of this account from the external source.
        :return: float balance
        """
        return Account._caller_0(self.__retrieve, self.__id)

    # Fund migration out-linking

    def get_transfer_to_function(self) -> callable:
        """
        Return the coupling to the fxn that transfers funds out of this account.
        :return: callable fxn
        """
        return self.__transfer_to

    def get_transfer_from_function(self) -> callable:
        """
        Return the coupling to the fxn that transfers funds into this account.
        :return: callable fxn
        """
        return self.__transfer_from

    def set_transfer_to_function(self, fxn: callable):
        """
        Set the coupling to the fxn that transfers funds out of this account.
        :param fxn: callable fxn
        """
        self.__transfer_to = fxn

    def set_transfer_from_function(self, fxn: callable):
        """
        Set the coupling to the fxn that transfers funds into this account.
        :param fxn: callable fxn
        """
        self.__transfer_from = fxn

    # Indirect transacting

    def make_deposit(self, deposit: float) -> bool:  # todo doc
        """"""
        if not self.__has_upper_bound or deposit + self.__holdings > self.__upper_bound:
            return False
        if Account._caller_1(self.__deposit, self.__id, deposit):
            self.__holdings += deposit
            return True
        return False

    def make_withdraw(self, withdraw: float) -> bool:
        """"""
        if not self.__has_lower_bound or self.__lower_bound > self.__holdings - withdraw:
            return False
        if Account._caller_1(self.__withdraw, self.__id, withdraw):
            self.__holdings -= withdraw
            return True
        return False

    # Direct transacting

    def set_balance(self, balance: float) -> bool:
        """"""
        if ((balance >= self.__lower_bound) if self.__lower_bound is not None else (
                (balance <= self.__upper_bound) if self.__upper_bound is not None else
                (self.__lower_bound <= balance <= self.__upper_bound))):
            if Account._caller_1(self.__override, self.__id, balance):
                self.__holdings = balance
                return True
        return False

    # Miscellaneous

    def get_balance(self) -> float:
        """"""
        return self.__holdings

    def get_id(self) -> int:
        """"""
        return self.__id

    # Abstract transacting

    # The exchange should occur in common currency units, like dollars.
    def migrate_holdings(self, destination: 'Account', amount: float) -> bool:
        """"""
        if self.__transfer_from is not None and destination.__transfer_to is not None and amount:
            if self.make_withdraw(amount):
                if destination.make_deposit(amount):
                    Account._caller_3(self.__transfer_from, self.__id, destination.get_id(), amount)
                    Account._caller_3(destination.__transfer_to, self.__id, destination.get_id(), amount)
                    return True
                else:
                    self.make_deposit(amount)
        return False


@unique
class PricePerSquareFootPhases(IntEnum):
    """
    Hold the phases for PricePerSquareFoot().
    Processing occurs in phases:
        0 Start(). Yes, it is necessary.
        1 Add locations.  Build the map, so to speak.
        2 Finalize that map.
        3 Add properties onto the map.
        4 Sort and finalize those properties.
        5 Calculate equities.
        6 Finalize equities.
        7 Finish(). Move onto an equity processor.
    """
    START = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    ADD_LOCATIONS = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    FINALIZE_LOCATIONS = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    ADD_PROPERTIES = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    FINALIZE_PROPERTIES = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    CALCULATE_EQUITIES = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    FINALIZE_EQUITIES = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()
    FINISH = IdSmuggler.PRICE_PER_SQUARE_FOOT_PHASES.next_id()

    def forward(self):
        """
        Return the phase after this one.
        :return: next phase
        """
        # noinspection PyBroadException
        try:
            return PricePerSquareFootPhases(self.value + 1)
        except Exception:
            return self


# for PricePerSquareFoot
address_to_location: callable = lambda address: reversed(address.split(', '))
location_to_address: callable = lambda location: ', '.join(str(y) for y in reversed(location))


class PricePerSquareFoot:
    """Find real estate deals more efficiently."""
    __listings: [(float, int, float, float)]  # price/sq.ft., property ID, price, sq. ft.
    __locations: dict  # area/zip codes in nested order:
    # For example, with {'a' : {'b' : 'c', 'd' : 'e'}, 'f' : 'g', 'h' : {'i' : 'j'}}:
    # C in under (inside) A.B, E's inside A.D, G's inside F, J's inside H.I, and A's inside None
    __equity: dict
    # With the above example:
    phase: PricePerSquareFootPhases
    __ids: int = 0

    def _advance_phase(self):
        """Go to the next phase."""
        self.phase = self.phase.forward()
        return

    def _phase_check(self, p: PricePerSquareFootPhases) -> bool:
        """
        Verify that phase p is not the current phase.
        :param p: a PricePerSquareFootPhases
        :return: bool
        """
        return self.phase != p

    def __init__(self):
        """Initialize to start accepting locations, and then properties."""
        self.phase = PricePerSquareFootPhases.START

    # START

    def start(self) -> bool:
        """
        Start() the process.
        Phase: START
        :return: successful or not
        """
        if self._phase_check(PricePerSquareFootPhases.START):
            return False
        self._advance_phase()
        self.__listings = []
        self.__locations = dict()
        self.__equity = dict()
        return True

    # ADD_LOCATIONS

    def add_location(self, location: [int]) -> bool:
        """
        Add a location to the map.  The location location is nested left to right or [0:].
        The location parameter is such that l[-1] is physically inside of l[-2], l[-2] is in l[-3], l[-3] in l[-4], and so on, ad infinitum.
        Another way to phrase the structure of the location argument is to state the l[0] contains (physically) l[1], l[1] contains l[2], l[2] has l[3], and so on.
        Phase: PricePerSquareFootPhases
        :param location: a nested [int] of area_codes/zip_codes
        :return: successful or not
        """
        if len(location) < 2:
            return False
        if self._phase_check(PricePerSquareFootPhases.ADD_LOCATIONS):
            return False
        self._advance_phase()
        outer: dict = self.__locations
        for container in location[:-1]:
            t: dict = outer.get(container)
            t2: dict = {}
            t3: bool = False
            if t is None:
                pass
            elif isinstance(t, dict):
                t2 = t
            else:
                t2 = {t: {}}
                t3 = True
            outer[container] = t2
            outer = t2[t] if t3 else t2
        if location[-1] not in outer.keys():
            outer[location[-1]] = None
        return True

    def get_location_map(self) -> dict:
        """"""
        if self._phase_check(PricePerSquareFootPhases.ADD_LOCATIONS):
            return {}
        return deepcopy(self.__locations)

    # FINALIZE_LOCATIONS

    # ADD_PROPERTIES

    def add_property(self, price: float, sq_ft: float, property_id: int = None) -> bool:
        """
        Add a "property" to the listings.  This "property" has attributes.
        Thee positive price price is a float in American dollars.
        The positive float sq_ft is the properties square foot.
        The property_id is just
        Phase: ADD_PROPERTIES
        :param price: its selling price
        :param sq_ft: its square footage
        :param property_id: its int ID.
        :return: successful or not
        """
        if self._phase_check(PricePerSquareFootPhases.ADD_PROPERTIES):
            return False
        self._advance_phase()
        self.__listings.append((round(price / sq_ft, 2), property_id if property_id is not None else IdSmuggler.PROPERTY_IDS.next_id(), price, sq_ft))  # price/sq.ft., property ID, price, sq. ft.
        return True

    # FINALIZE_PROPERTIES

    def sort_properties(self) -> bool:
        """
        Sort the listings in order of least square foot first to greatest last.
        Phase: FINALIZE_PROPERTIES
        :return: successful or not
        """
        if self._phase_check(PricePerSquareFootPhases.FINALIZE_PROPERTIES):
            return False
        self._advance_phase()
        self.__listings.sort()
        return True

    # CALCULATE_EQUITIES

    # FINALIZE_EQUITIES

    # FINISH
