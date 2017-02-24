#include "ValueRefParserImpl.h"


namespace {
    struct simple_int_parser_rules {
        simple_int_parser_rules() {
            qi::_1_type _1;
            qi::_val_type _val;
            using phoenix::new_;

            const parse::lexer& tok =   parse::lexer::instance();

            // TODO: Should we apply elements of this list only to certain
            // objects? For example, if one writes "Source.Planet.",
            // "NumShips" should not follow.
            bound_variable_name
                =   tok.Owner_
                |   tok.SupplyingEmpire_
                |   tok.ID_
                |   tok.CreationTurn_
                |   tok.Age_
                |   tok.ProducedByEmpireID_
                |   tok.ArrivedOnTurn_
                |   tok.DesignID_
                |   tok.FleetID_
                |   tok.PlanetID_
                |   tok.SystemID_
                |   tok.FinalDestinationID_
                |   tok.NextSystemID_
                |   tok.NearestSystemID_
                |   tok.PreviousSystemID_
                |   tok.NumShips_
                |   tok.NumStarlanes_
                |   tok.LastTurnBattleHere_
                |   tok.LastTurnActiveInBattle_
                |   tok.Orbit_
                |   tok.SpeciesID_
                |   tok.TurnsSinceFocusChange_
                |   tok.ETA_
                ;

            constant
                =   tok.int_    [ _val = new_<ValueRef::Constant<int> >(_1) ]
                ;

            free_variable_name
                =   tok.CurrentTurn_
                |   tok.GalaxyAge_
                |   tok.GalaxyMaxAIAggression_
                |   tok.GalaxyMonsterFrequency_
                |   tok.GalaxyNativeFrequency_
                |   tok.GalaxyPlanetDensity_
                |   tok.GalaxyShape_
                |   tok.GalaxySize_
                |   tok.GalaxySpecialFrequency_
                |   tok.GalaxyStarlaneFrequency_
                ;

            free_variable
                =   tok.Value_
                    [ _val = new_<ValueRef::Variable<int> >(ValueRef::EFFECT_TARGET_VALUE_REFERENCE) ]
                |   free_variable_name
                    [ _val = new_<ValueRef::Variable<int> >(ValueRef::NON_OBJECT_REFERENCE, _1) ]
                ;

            simple
                =   constant
                |   free_variable
                |   bound_variable
                ;

            initialize_bound_variable_parser<int>(bound_variable, bound_variable_name);

            free_variable_name.name("integer free variable name (e.g. CurrentTurn)");
            bound_variable_name.name("integer bound variable name (e.g., FleetID)");
            constant.name("integer constant");
            free_variable.name("free integer variable");
            bound_variable.name("bound integer variable");
            simple.name("simple integer expression (constant, free or bound variable)");

#if DEBUG_VALUEREF_PARSERS
            debug(free_variable_name);
            debug(bound_variable_name);
            debug(constant);
            debug(free_variable);
            debug(bound_variable);
            debug(simple);
#endif
        }

        name_token_rule     free_variable_name;
        name_token_rule     bound_variable_name;
        parse::value_ref_rule<int> constant;
        variable_rule<int>  free_variable;
        variable_rule<int>  bound_variable;
        parse::value_ref_rule<int> simple;
    };

    simple_int_parser_rules& get_simple_int_parser_rules() {
        static simple_int_parser_rules retval;
        return retval;
    }

    struct int_parser_rules {
        int_parser_rules() {

            const parse::value_ref_rule<int>& simple = int_simple();

            statistic_sub_value_ref
                =   simple
                |   int_var_complex()
            ;

            initialize_numeric_statistic_parser<int>(statistic, statistic_1, statistic_2,
                                                     statistic_sub_value_ref);

            initialize_numeric_expression_parsers<int>(function_expr,
                                                       exponential_expr,
                                                       multiplicative_expr,
                                                       additive_expr,
                                                       expr,
                                                       primary_expr);

            primary_expr
                =   '(' >> expr >> ')'
                |   simple
                |   statistic
                |   int_var_complex()
                ;

            statistic_1.name("integer collection statistic");
            statistic_2.name("integer value statistic");
            statistic.name("integer statistic");
            statistic_sub_value_ref.name("integer statistic value ref");
            function_expr.name("integer function expression");
            exponential_expr.name("integer exponential expression");
            multiplicative_expr.name("integer multiplication expression");
            additive_expr.name("integer additive expression");
            expr.name("integer expression");
            primary_expr.name("integer expression");

#if DEBUG_VALUEREF_PARSERS
            debug(statistic);
            debug(negate_expr);
            debug(multiplicative_expr);
            debug(additive_expr);
            debug(expr);
            debug(primary_expr);
#endif
        }

        statistic_rule<int> statistic_1;
        statistic_rule<int> statistic_2;
        statistic_rule<int> statistic;
        parse::value_ref_rule<int> statistic_sub_value_ref;
        expression_rule<int> function_expr;
        expression_rule<int> exponential_expr;
        expression_rule<int> multiplicative_expr;
        expression_rule<int> additive_expr;
        parse::value_ref_rule<int> expr;
        parse::value_ref_rule<int> primary_expr;
    };

    int_parser_rules& get_int_parser_rules() {
        static int_parser_rules retval;
        return retval;
    }

    struct castable_as_int_parser_rules {
        castable_as_int_parser_rules() {
            qi::_1_type _1;
            qi::_val_type _val;
            using phoenix::new_;

            castable_expr
                = parse::double_value_ref() [ _val = new_<ValueRef::StaticCast<double, int> >(_1) ]
                ;

            flexible_int 
                = parse::int_value_ref()
                | castable_expr
                ;

            castable_expr.name("castable as integer expression");
            flexible_int.name("integer or castable as integer");

#if DEBUG_VALUEREF_PARSERS
            debug(castable_expr);
#endif
        }

        parse::value_ref_rule<int> castable_expr;
        parse::value_ref_rule<int> flexible_int;
    };

    castable_as_int_parser_rules& get_castable_as_int_parser_rules() {
        static castable_as_int_parser_rules retval;
        return retval;
    }
}


const variable_rule<int>& int_bound_variable()
{ return get_simple_int_parser_rules().bound_variable; }

const variable_rule<int>& int_free_variable()
{ return get_simple_int_parser_rules().free_variable; }

const parse::value_ref_rule<int>& int_simple()
{ return get_simple_int_parser_rules().simple; }

const statistic_rule<int>& int_var_statistic()
{ return get_int_parser_rules().statistic; }


namespace parse {
    value_ref_rule<int>& int_value_ref()
    { return get_int_parser_rules().expr; }

    value_ref_rule<int>& flexible_int_value_ref()
    { return get_castable_as_int_parser_rules().flexible_int; }
}
