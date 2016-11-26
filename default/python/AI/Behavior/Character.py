"""
Character represents the personalization of the AI.

Character is composed of orthogonal elements called Behavior.  Behavior
elements are orthogonal, which means that they do not interact and can be
freely mixed and matched to create a Character.  Orthogonality means
that they can be tested independently and combined with simple
combiners.

Character creates big changes in the behavior of the AI that are visible
to the player as personality.  At key/tap points the AI checks the character
for permission 'may_<do something>' or preference of a series of
alternative actions 'prefer_<somethings>'.  Preference could be expanded
to look at all of the options and remove those that the behavior
forbids.

Permission type taps are named may_<do something>(information needed to decide).
The behavior examines the information and returns true if that action is permitted.

Preference type taps are named prefer_<somethings>(alternatives, extra info).
Alternatives is a list of all possible actions.  The behavior examines all
the alternatives and returns a possibly empty list of the permissible
actions.

Character should be invoked by other modules at key behavioral tap points to
provide direction not optimization.  For example which empire/species do
I love/hate enough to attack.

The gated behaviors should be big user discernable changes, not small
coefficient optimizations better handled with a local optimization
routine. If there are setup options to the behavior they should fall
into 2 (on/off) or 3 settings.  For example,
deceitful/typical/trustworthy.  The idea is not to create deep, subtle,
nuanced personalities, but writ large Shakespearean characters that draw the
player into the narrative structure of the particular game that they are playing.

Each AI will get the mandatory behavior (probably Difficulty/Challenge)
and a selection of the optional behaviors.

There is no need for per species behavior.  Each playable species can be
assigned some additional mandatory behavior(s).  For example the Trith and
a mandatory Genocidal behavior.  Perhaps add a probabilty distribution of
behavior components to the FOCS description of a playable species.
"""


# Some ideas for future behavior modules are:
# TODO: challenge/difficulty -- to replace the difficulty related portions
#                                of aggression.
#
# TODO: research bent -- models an obsession/focus/repulsion by a particular
# area of research. i.e. Shields are for grues.
#
# TODO: nemesis/single-minded -- model a focus on a single opponent, perhaps
# the first one to attack the AI.  This plays well with CharacterStrings
# which can be used to inform all players who care that "I will hunt the
# Dominion to the ends of the galaxy."  Humans and eventually AIs could
# use this to modify their risk assessment of this AI.
#
# TODO: deceitful/trustworthy -- Only useful after treaties are implemented to
# determine if this AI will abide by the treaty
#
# TODO: friendly and loyal -- Even without treaties this AI will assist their
# friends.
#
# TODO: vengeful -- An eye for eye.  AI generally counter attacks until things
# are made right or even.
#
# TODO: risk averse/gambler -- How much overkill does the AI require?  How risky
# a research strategy will it attempt?  How many redundant buildings does
# the AI build?
#
# TODO: warlike/peaceful -- Will the AI prefer colonization to war?
#
# TODO: cooperative/loner -- Once cooperative treaties (joint attack, sharing
# system) are implemented, will the AI use them?
#
# TODO: taciturn/chatty -- How often does the AI chat?
#
# TODO: genocidal -- Will the AI research and use Concentration Camps/bombard
# weapons/planet and star destroying weapons?  Is the AI horrified by the
# use of such weapons?  Will the AI band together with other like minded
# empires to protect the galaxy?
#


import abc
from collections import Counter
import random

import freeOrionAIInterface as fo  # pylint: disable=import-error


class Behavior(object):
    """An abstract class representing a type of behavior of the AI.

    Behaviors give the AI personality along some dimension.
    Behaviors do not help the AI make optimal decisions, they determine whether
    certain actions are permissible or preferable.

    Behaviors are combined to form a single Character.

    Behaviors have taps which the AI calls to determine it behavior with
    respect to a single action.  There are two types of taps: permission
    taps which permit/forbid an action and preference taps which indicate
    which of several alternatives are permissible.

    Permission type taps are named may_<do something>(information needed to decide).
    The behavior examines the information and returns true if that action is
    permitted.

    Preference type taps are named prefer_<somethings>(alternatives, extra info).
    Alternatives is a list of all possible actions.  The behavior examines all of
    the alternatives and returns a possibly empty list of the permissible actions.

    Any given Behavior class should not implement all the taps, only those
    it needs to override to cause the relevant behavior.
    """
    __metaclass__ = abc.ABCMeta

    def __repr__(self):
        return "Behavior"

    # @abc.abstractproperty
    @property
    def key(self):  # pylint: disable=no-self-use,unused-argument
        """Return a key to be used as an index into look up tables.

        For example, a string table of 6 diplomatic responses bases on aggression might look like:

        table_x = {fo.aggression.beginner: "DIPLO_X_BEGINNER",
                   fo.aggression.turtle: "DIPLO_X_TURTLE",
                   fo.aggression.cautious: "DIPLO_X_CAUTIOUS",
                   fo.aggression.typical: "DIPLO_X_TYPICAL",
                   fo.aggression.aggressive: "DIPLO_X_AGGRESSIVE",
                   fo.aggression.maniacal: "DIPLO_X_MANIACAL"}

        Using the key to fetch a single string from that table_x looks like:

        used_string_x = table_x[character.get_behavior(Character.Behavior.Aggression).key]

        See CharacterStrings.py for the details of this actual example.

        """
        return None

    def may_explore_system(self, monster_threat):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to explore system with the given monster threat."""
        return True

    def may_surge_industry(self, totalPP, totalRP):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to surge industry as used in PriorityAI.py"""
        return True

    def may_maximize_research(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to maximize research."""
        return True

    def preferred_research_cutoff(self, alternatives):  # pylint: disable=no-self-use,unused-argument
        """Return preferred research cutoff from the list of alternatives."""
        # TODO Remove this tap it is one of the empire id dependent taps. See EmpireIDBehavior.
        return None

    def max_number_colonies(self):  # pylint: disable=no-self-use,unused-argument
        """Return maximum allowed number of colonies"""
        return 1000000

    def may_invade(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to invade."""
        return True

    def may_invade_with_bases(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to invade with bases."""
        return True

    def invasion_priority_scaling(self):  # pylint: disable=no-self-use,unused-argument
        return 1.0

    def military_priority_scaling(self):  # pylint: disable=no-self-use,unused-argument
        return 1.0

    def preferred_colonization_portion(self, alternatives):  # pylint: disable=no-self-use,unused-argument
        """Select from the fractions in alternatives the fraction of PP to be spend on colonization."""
        # TODO Remove this tap it is one of the empire id dependent taps. See EmpireIDBehavior.
        return None

    def preferred_outpost_portion(self, alternatives):  # pylint: disable=no-self-use,unused-argument
        """Select from the fractions in alternatives the fraction of PP to be spend on outposts."""
        # TODO Remove this tap it is one of the empire id dependent taps. See EmpireIDBehavior.
        return None

    def preferred_building_ratio(self, alternatives):  # pylint: disable=no-self-use,unused-argument
        """Select a fraction less than 1 from alternatives as the maximum ratio of PP for buildings"""
        # TODO Remove this tap it is one of the empire id dependent taps. See EmpireIDBehavior.
        return None

    def preferred_discount_multiplier(self, alternatives):  # pylint: disable=no-self-use,unused-argument
        """Select a discount multiplier from the alternatives provided for
        use in evaluate planet in Colonisation.py to scale pilot rating and
        a long list of technologies.
        """
        # TODO Remove this tap it is one of the empire id dependent taps. See EmpireIDBehavior.
        return None

    def max_defense_portion(self):  # pylint: disable=no-self-use,unused-argument
        """Return maximum fraction of production for defense"""
        return 1.0

    def check_orbital_production(self):  # pylint: disable=no-self-use,unused-argument
        """Return true if orbital defense production should be checked this turn in ProductionAI.py"""
        return False

    def target_number_of_orbitals(self):  # pylint: disable=no-self-use,unused-argument
        """Return target number of orbitals defenses to be built."""
        return 0

    def may_build_building(self, building):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to build ''building''"""
        return True

    def may_produce_troops(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to produce troop ships"""
        return True

    def military_safety_factor(self):  # pylint: disable=no-self-use,unused-argument
        """Return military safety factor, the ratio of
        (enemy strength) / (own strength) that the AI considers acceptable risk.
        """
        return 0.0

    def may_dither_focus_to_gain_research(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to trade production at a loss for research"""
        return True

    def may_research_heavily(self):  # pylint: disable=no-self-use,unused-argument
        """Return true if allowed to target research/industry > 1.5"""
        return True

    def may_travel_beyond_supply(self, distance):  # pylint: disable=no-self-use,unused-argument
        """Return True if able to travel distance hops beyond empire supply"""
        # TODO Remove this tap it is one of the empire id dependent taps. See EmpireIDBehavior.
        return True

    def get_research_index(self):  # pylint: disable=no-self-use,unused-argument
        """Deprecated.  Only used with old style research."""
        # TODO Remove this tap when old style research is removed.
        return None

    def may_research_xeno_genetics_variances(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if AI if allowed to research xeno genetics research 'Dep.GRO_XENO_GENETICS'."""
        # TODO remove this as overly specific
        return True

    def prefer_research_defensive(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if should prefer defensive tech research"""
        return True

    def prefer_research_low_aggression(self):  # pylint: disable=no-self-use,unused-argument
        """Return True if should prefer less aggressive tech research"""
        return True

    def may_research_tech(self, tech):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to research ''tech''. This is only called by the new research algorithm."""
        return True

    def may_research_tech_classic(self, tech):  # pylint: disable=no-self-use,unused-argument
        """Return True if permitted to research ''tech''.  This is called in the classic research algorithm."""
        # TODO remove this tap when the classic research algorithm is removed.
        return True

    def attitude_to_empire(self, other_empire_id, diplomatic_logs):  # pylint: disable=no-self-use,unused-argument
        """Return a value from [-10 .. 10] representing attitude towards other empire."""
        return None

    def warship_adjusted_production_cost_exponent(self):  # pylint: disable=no-self-use,unused-argument
        """Return an exponent to scale the production cost of a warship in ShipDesignAI."""
        return None


class Aggression(Behavior):
    """A behavior that models level of difficulty and aggression."""

    # The initial implementation was to pull aggression dependent code from
    # the main body of code into this behavior Aggression.  These are merely
    # refactoring of existing code and is not an example of ideal
    # implementation.

    # Aggression implements two different behaviors as one: difficulty and
    # aggression.  It creates too many decision points not clearly related to
    # either concept.  Aggression should be broken into two behaviors:
    # difficulty/challenge and aggression.

    # TODO break this class into two behaviors: level of difficulty and aggression

    def __init__(self, aggression):
        self.aggression = aggression

    @property
    def key(self):
        return self.aggression

    def may_explore_system(self, monster_threat):
        return monster_threat < 2000 * self.aggression

    def may_surge_industry(self, total_pp, total_rp):
        return ((self.aggression > fo.aggression.cautious) and
                ((total_pp + 1.6 * total_rp) < (50 * self.aggression)))

    def may_maximize_research(self):
        return self.aggression >= fo.aggression.maniacal

    def max_number_colonies(self):
        # significant growth barrier for low aggression, negligible for high aggression
        return 2 + ((0.5 + self.aggression) ** 2) * fo.currentTurn() / 50.0

    def may_invade(self):
        return (self.aggression > fo.aggression.turtle
                and not (self.aggression == fo.aggression.beginner and fo.currentTurn() < 150))

    def may_invade_with_bases(self):
        return self.aggression > fo.aggression.typical

    def invasion_priority_scaling(self):
        return 0.5 if self.aggression == fo.aggression.beginner else 1.0

    def military_priority_scaling(self):
        return (1.0 if self.aggression > fo.aggression.typical
                else ((1.0 + self.aggression) / (1.0 + fo.aggression.typical)))

    def max_defense_portion(self):
        return [0.7, 0.4, 0.3, 0.2, 0.1, 0.0][self.aggression]

    def check_orbital_production(self):
        aggression_index = max(1, self.aggression)
        return ((fo.currentTurn() % aggression_index) == 0) and self.aggression < fo.aggression.maniacal

    def target_number_of_orbitals(self):
        aggression_index = max(1, self.aggression)
        return min(int(((fo.currentTurn() + 4) / (8.0 * aggression_index ** 1.5)) ** 0.8),
                   fo.aggression.maniacal - aggression_index)

    BUILDING_TABLE_STATIC = {"BLD_SHIPYARD_AST": fo.aggression.beginner,
                             "BLD_GAS_GIANT_GEN": fo.aggression.beginner,
                             "BLD_SOL_ORB_GEN": fo.aggression.turtle,
                             "BLD_ART_BLACK_HOLE": fo.aggression.typical,
                             "BLD_BLACK_HOLE_POW_GEN": fo.aggression.cautious,
                             "BLD_CONC_CAMP": fo.aggression.typical,
                             "BLD_SHIPYARD_CON_NANOROBO": fo.aggression.aggressive,
                             "BLD_SHIPYARD_CON_GEOINT": fo.aggression.aggressive,
                             # TODO determine which duplicate of BLD_SHIPYARD_AST is correct
                             # "BLD_SHIPYARD_AST": fo.aggression.typical,
                             "BLD_SHIPYARD_AST_REF": fo.aggression.maniacal,
                             "BLD_SHIPYARD_ORG_CELL_GRO_CHAMB": fo.aggression.aggressive,
                             "BLD_SHIPYARD_ORG_XENO_FAC": fo.aggression.aggressive,
                             "BLD_SHIPYARD_ENRG_COMP": fo.aggression.aggressive,
                             "BLD_SHIPYARD_ENRG_SOLAR": fo.aggression.maniacal,
                             "BLD_NEUTRONIUM_FORGE": fo.aggression.cautious}

    @property
    def building_table(self):
        return type(self).BUILDING_TABLE_STATIC

    def may_build_building(self, building):
        return self.aggression > self.building_table.get(building, fo.aggression.beginner)

    def may_produce_troops(self):
        # TODO check if this is consitent with may invade
        return self.aggression >= fo.aggression.typical

    def military_safety_factor(self):
        return [4.0, 3.0, 2.0, 1.5, 1.2, 1.0][self.aggression]

    def may_dither_focus_to_gain_research(self):
        return self.aggression < fo.aggression.aggressive

    def may_research_heavily(self):
        return self.aggression > fo.aggression.cautious

    def may_research_xeno_genetics_variances(self):
        return self.aggression >= fo.aggression.cautious

    def prefer_research_defensive(self):
        return self.aggression <= fo.aggression.cautious

    def prefer_research_low_aggression(self):
        return self.aggression < fo.aggression.typical

    tech_lower_threshold_static = {"LRN_TRANSCEND": fo.aggression.aggressive}

    def may_research_tech(self, tech):
        return type(self).tech_lower_threshold_static.get(tech, fo.aggression.beginner) <= self.aggression

    TECH_UPPER_THRESHOLD_CLASSIC_STATIC = {"DEF_DEFENSE_NET_1": fo.aggression.cautious,
                                           "DEF_GARRISON_1": fo.aggression.cautious,
                                           "GRO_XENO_GENETICS": fo.aggression.cautious,
                                           "GRO_GENETIC_ENG": fo.aggression.cautious}

    TECH_LOWER_THRESHOLD_CLASSIC_STATIC = {"SHP_DEFLECTOR_SHIELD": fo.aggression.aggressive,
                                           "CON_ARCH_PSYCH": fo.aggression.aggressive,
                                           "CON_CONC_CAMP": fo.aggression.aggressive,
                                           "LRN_XENOARCH": fo.aggression.typical,
                                           "LRN_PHYS_BRAIN": fo.aggression.typical,
                                           "LRN_TRANSLING_THT": fo.aggression.typical,
                                           "LRN_PSIONICS": fo.aggression.typical,
                                           "LRN_DISTRIB_THOUGHT": fo.aggression.typical,
                                           "LRN_QUANT_NET": fo.aggression.typical,
                                           "PRO_SINGULAR_GEN": fo.aggression.typical,
                                           "LRN_TRANSCEND": fo.aggression.typical}

    def may_research_tech_classic(self, tech):
        return (type(self).TECH_LOWER_THRESHOLD_CLASSIC_STATIC.get(tech, fo.aggression.beginner)
                <= self.aggression <=
                type(self).TECH_UPPER_THRESHOLD_CLASSIC_STATIC.get(tech, fo.aggression.maniacal))

    def attitude_to_empire(self, other_empire_id, diplomatic_logs):
        # TODO: In other behaviors consider proximity, competitive
        # needs, relations with other empires, past history with this
        # empire, etc.
        # in the meantime, somewhat random
        # TODO: Move the diplomatic log portion of this behavior back
        # into diplomacy where it belongs.
        if self.aggression == fo.aggression.maniacal:
            return -9
        if self.aggression == fo.aggression.beginner:
            return 9
        log_index = (other_empire_id, fo.empireID())
        num_peace_requests = len(diplomatic_logs.get('peace_requests', {}).get(log_index, []))
        num_war_declarations = len(diplomatic_logs.get('war_declarations', {}).get(log_index, []))
        # Too many requests for peace irritate the AI, as do any war declarations
        irritation = (self.aggression * (2.0 + num_peace_requests / 10.0 + 2.0 * num_war_declarations) + 0.5)
        attitude = 10 * random.random() - irritation
        return min(10, max(-10, attitude))

    def warship_adjusted_production_cost_exponent(self):  # pylint: disable=no-self-use,unused-argument
        # as military ships are grouped up in fleets, their power rating scales quadratic in numbers.
        # To account for this, we need to maximize rating/cost_squared not rating/cost as usual.
        if self.aggression == fo.aggression.maniacal:
            exponent = 2.0
        elif self.aggression == fo.aggression.aggressive:
            exponent = 1.5
        else:
            exponent = 1.0
        return exponent


class EmpireIDBehavior(Behavior):
    """A behavior that models empire id influence.
    Mostly some modulo 2 effects."""

    # The initial implementation was to pull empire.id modulo 2 or 3 optional
    # portions of the code into this behavior EmpireIDBehavior.  This was
    # merely a refactoring of existing code and is not an example of ideal
    # implementation.

    # EmpireID selects based on empire.id with is an implementation detail and
    # not a "visible" game mechanic.  EmpireID is also used to select between
    # coefficient options, which look like programmer experiments.  EmpireID
    # should be removed as a behavior.

    # TODO: Remove EmpireIDBehavior.
    # Empire id is a game mechanic.  It is not something that a player
    # can describe, "Look the 'Continuum' is behaving like a 1 modulo 2 character."

    def __init__(self, empire_id, aggression):
        print "EmpireIDBehavior initialized."
        self.id = empire_id
        self.aggression = aggression  # TODO remove when old research style get_research_index is removed

    @property
    def key(self):
        return self.id % 2

    def _modulo_two_choice(self, alternatives):
        if not alternatives:
            return None
        if len(alternatives) == 1:
            return alternatives[0]
        return alternatives[self.id % 2]

    def preferred_research_cutoff(self, alternatives):
        return self._modulo_two_choice(alternatives)

    def preferred_colonization_portion(self, alternatives):
        return self._modulo_two_choice(alternatives)

    def preferred_outpost_portion(self, alternatives):
        return self._modulo_two_choice(alternatives)

    def preferred_building_ratio(self, alternatives):
        if not alternatives:
            return None
        return alternatives[self.id % 3] if len(alternatives) >= 3 else alternatives[self.id % len(alternatives)]

    def preferred_discount_multiplier(self, alternatives):
        return self._modulo_two_choice(alternatives)

    def may_travel_beyond_supply(self, distance):
        return (distance < 2
                or distance <= 2 and self.aggression >= fo.aggression.typical
                or self.aggression >= fo.aggression.aggressive)

    # TODO remove this function as soon as old style research is gone
    # It defeats the orthogonality goal of character components for little gain
    def get_research_index(self):
        research_index = self.id % 2
        if self.aggression >= fo.aggression.aggressive:
            research_index = 2 + (self.id % 3)  # so indices [2,3,4]
        elif self.aggression >= fo.aggression.typical:
            research_index += 1
        return research_index


class Character(Behavior):
    """
    A collection of behaviours.

    For each query that Behavior supports a Character queries
    all of its own behaviors to determine if an action is permissible or prefered.
    """

    def __init__(self, behaviors):
        self.behaviors = behaviors
        if not all([isinstance(x, Behavior) for x in behaviors]):
            raise TypeError("All behaviors must be sub-classes of Behavior")

    def get_behavior(self, type_of_behavior):
        """Return the requested behavior or None"""
        behavior = [x for x in self.behaviors if isinstance(x, type_of_behavior)]
        return behavior[0] if behavior else Behavior()


# Complete the Character class by adding all of the combiners to combine the outputs of the
# individual behaviors.  Character tries to combine results in the way most limiting to the AI

def _make_single_function_combiner(funcnamei, f_combo):
    """Make a combiner that collects the results of funcname from each behavior
    and applies f_combo to the results"""
    def func(self, *args, **kwargs):
        """Apply funcnamei to each behavior and combine them with ''f_combo''"""
        return f_combo([getattr(x, funcnamei)(*args, **kwargs) for x in self.behaviors])
    return func

# Create combiners for behaviors that all must be true
for funcname in ["may_explore_system", "may_surge_industry", "may_maximize_research", "may_invade",
                 "may-invade_with_bases", "may_build_building", "may_produce_troops",
                 "may_dither_focus_to_gain_research", "may_research_heavily",
                 "may_travel_beyond_supply", "may_research_xeno_genetics_variances",
                 "prefer_research_defensive", "prefer_research_low_aggression", "may_research_tech",
                 "may_research_tech_classic"]:
    setattr(Character, funcname, _make_single_function_combiner(funcname, all))

# Create combiners for behaviors that take min result
for funcname in ["max_number_colonies", "invasion_priority_scaling",
                 "military_priority_scaling", "max_defense_portion"]:
    setattr(Character, funcname, _make_single_function_combiner(funcname, min))

# Create combiners for behaviors that take max result
for funcname in ["target_number_of_orbitals", "military_safety_factor", "get_research_index"]:
    setattr(Character, funcname, _make_single_function_combiner(funcname, max))

# Create combiners for behaviors that take any result
for funcname in ["check_orbital_production"]:
    setattr(Character, funcname, _make_single_function_combiner(funcname, any))


# Create combiners for behaviors that averages all not None results
def average_not_none(llin):
    ll = [x for x in llin if x]
    return sum(ll) / len(ll)

for funcname in ["attitude_to_empire", "warship_adjusted_production_cost_exponent"]:
    setattr(Character, funcname, _make_single_function_combiner(funcname, average_not_none))


def _make_most_preferred_combiner(funcnamei):
    """Make a combiner that runs the preference function for each behavior and
    returns the result most preferred by all the behaviors."""
    def _most_preferred(self, alternatives):
        """Applies funcnamei from each behavior to the alternatives and return the most preferred."""
        prefs = [y for y in [getattr(x, funcnamei)(alternatives) for x in self.behaviors] if y is not None]
        if not prefs:
            return None
        if len(prefs) == 1:
            return prefs[0]
        return Counter.most_common(Counter(prefs), 1)[0][0]
    return _most_preferred

# Create combiners for behaviors deal with preference
for funcname in ["preferred_research_cutoff", "preferred_colonization_portion",
                 "preferred_outpost_portion", "preferred_building_ratio", "preferred_discount_multiplier"]:
    setattr(Character, funcname, _make_most_preferred_combiner(funcname))


def create_character(aggression=fo.aggression.maniacal, empire_id=0):
    """Create a character."""
    # TODO add the mandatory (Difficulty) and optional/random (everything
    # else) interface to Character creation.

    # Check the optionsDB for the behavior bypass values and create
    # the character.
    NO_VALUE = -1
    bypassed_aggression = get_behavior_bypass_value("aggression", aggression, NO_VALUE)
    bypassed_empire_id = get_behavior_bypass_value("empire-id", empire_id, NO_VALUE)

    return Character([Aggression(bypassed_aggression), EmpireIDBehavior(bypassed_empire_id, bypassed_aggression)])


def get_behavior_bypass_value(name, default, sentinel):
    """Fetch a bypassed behavior value or return the default from OptionsDB.

    In OptionsDB a section AI.config.behavior can contain default behavior
    values for all of the AIs or specific AIs which will override the
    default value passed into this function.

    If there is an XML element in config.xml/persistent_config.xml
    AI.config.behavior.<name of behavior here>.force
    with a non zero value

    ,then the value of AI.config.behavior.<name of behavior here>.<AI ID number here>

    will be checked.  If it is not the sentinel value (typically -1) the it
    will be returned as the behavior's value.

    Otherwise the value of
    AI.config.behavior.<name of behavior here>.all
    is checked.  Again if it is not the sentinel value it will ovverride
    the returned value for behavior.

    If behavior is not overriden by one of the above values, then the
    default is used.

    Here is an example section providing override values aggression and the
    empire-id behavior.

    <mAI>
      <config>
        <behavior>
          <aggression>
            <force>1</force>
            <all>4</all>
            <AI_0>5</AI_0>
            <AI_1>4</AI_1>
            <AI_2>3</AI_2>
            <AI_3>2</AI_3>
            <AI_4>1</AI_4>
            <AI_5>0</AI_5>
          </aggression>
          <empire-id>
            <force>1</force>
            <AI_0>5</AI_0>
            <AI_1>4</AI_1>
            <AI_2>3</AI_2>
            <AI_3>2</AI_3>
            <AI_4>1</AI_4>
            <AI_5>0</AI_5>
          </empire-id>
        </behavior>
      </config>
    </mAI>

    :param name: Name of the behavior.
    :type name: string
    :param default: Default value of the behavior.
    :type default: int
    :param sentinel: A value indicating no valid value.
    :type sentinel: int
    :return: The behavior
    :rtype: Behavior

    """

    force_option = "AI.config.behavior.%s.force" % (name,)
    if not fo.getOptionsDBOptionBool(force_option):
        return default

    per_id_option = "AI.config.behavior.%s.%s" % (name, fo.playerName())
    all_id_option = "AI.config.behavior.%s.all" % (name,)

    behavior = fo.getOptionsDBOptionInt(per_id_option)
    if behavior is None or behavior == sentinel:
        behavior = fo.getOptionsDBOptionInt(all_id_option)

    if behavior is None or behavior == sentinel:
        behavior = default
    else:
        print "%s behavior bypassed and set to %s for %s" % (name, repr(behavior), fo.playerName())
    return behavior
