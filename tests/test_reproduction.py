from pathlib import Path
import json
from wh_reference.reproduce import reproduce

ROOT=Path(__file__).resolve().parents[1]
R=reproduce(ROOT/'data')

def frac(x): return f"{x['n']}/{x['d']}"

def test_p1_headline():
    p=R['protocol_1']
    assert frac(p['detection_sensitivity'])=='77/81'
    assert frac(p['specificity'])=='18/19'
    assert frac(p['exact_fault_set_localization'])=='52/61'
    assert frac(p['topology_classification'])=='78/100'
    assert frac(p['appropriate_abstention'])=='20/20'
    assert p['governance_violations']==0

def test_p1_failure_boundary_preserved():
    n=R['protocol_1']['novel_block']
    assert frac(n['detection'])=='17/20'
    assert frac(n['localization'])=='12/20'
    assert frac(n['topology'])=='0/20'

def test_p2_final_panel_and_regression():
    p=R['protocol_2']
    assert f"{p['correct']}/{p['N']}"=='240/240'
    assert p['regression_tests_passed']==175
    assert p['governance_violations_from_rows']==0

def test_p2_key_endpoints():
    k=R['protocol_2']['key_endpoints']
    assert (k['known_class_retention'],k['known_class_n'])==(20,20)
    assert (k['new_combination_accuracy'],k['new_combination_n'])==(20,20)
    assert (k['underdetermined_correct'],k['underdetermined_n'])==(40,40)
    assert (k['nonnovel_control_correct'],k['nonnovel_control_n'])==(60,60)
    assert (k['minimal_core_exact'],k['minimal_core_n'])==(20,20)
    assert (k['characterization_chain_correct'],k['characterization_chain_n'])==(40,40)
    assert (k['governed_learning_reuse_success'],k['governed_learning_reuse_n'])==(20,20)
    assert (k['pseudoreplication_holds'],k['pseudoreplication_n'])==(20,20)

def test_comparator_detection_gradient():
    c=R['protocol_3_comparator']
    assert frac(c['FOC']['failure_detection_sensitivity'])=='23/28'
    assert frac(c['MLC']['failure_detection_sensitivity'])=='28/28'
    assert frac(c['WH']['failure_detection_sensitivity'])=='28/28'

def test_comparator_localization_gradient():
    c=R['protocol_3_comparator']
    assert frac(c['FOC']['exact_fault_set_localization'])=='0/20'
    assert frac(c['MLC']['exact_fault_set_localization'])=='8/20'
    assert frac(c['WH']['exact_fault_set_localization'])=='20/20'

def test_comparator_higher_order_and_repair_safety():
    w=R['protocol_3_comparator']['WH']
    assert frac(w['higher_order_correct_resolution'])=='24/24'
    assert frac(w['repair_target_coverage'])=='12/12'
    assert frac(w['unsupported_repair_target'])=='0/20'
    assert w['inspection_count']==4

def test_healthy_transfer():
    b=R['protocol_3_healthy_transfer']
    assert frac(b['healthy_false_failure'])=='0/8'
    assert frac(b['benign_variation_false_failure'])=='0/4'
    assert b['reference_difference_cases_accepted']==len(b['reference_difference_cases'])==3
    assert b['representation_leakage_terms']==[]
    assert b['governance_violations']==0

def test_foreign_failure_transfer():
    b=R['protocol_3_foreign_failure']
    assert frac(b['failure_detection_sensitivity'])=='20/20'
    assert frac(b['exact_fault_localization_eligible'])=='16/16'
    assert frac(b['topology_or_disposition_correctness'])=='20/20'
    assert frac(b['appropriate_hold_abstain'])=='2/2'
    assert frac(b['false_resolution_novel_or_underdetermined'])=='0/4'
    assert frac(b['unsupported_repair_target'])=='0/12'
    assert b['representation_leakage_terms']==[]
    assert b['governance_violations']==0

def test_r3_closed_only_after_reaudit():
    r=R['r3']
    assert r['human_gate_decision']=='AUTHORIZE_SANDBOX_TRIAL'
    assert frac(r['acceptance_checks'])=='6/6'
    assert r['protected_artifacts_unchanged'] is True
    assert r['closure_state']=='RESOLVED'
    assert r['production_promotion_state']=='NOT_PROMOTED_TO_PRODUCTION'
    assert r['closed'] is True
