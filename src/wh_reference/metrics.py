from __future__ import annotations
from collections import defaultdict
import re
from .io import as_set, ratio


def score_p1(truth_obj, pred_obj):
    truth = truth_obj["cases"]
    preds = {x["case_id"]: x for x in pred_obj["cases"]}
    TP=TN=FP=FN=0
    exact_loc=loc_den=topo_ok=action_ok=0
    abstain_ok=abstain_n=overclaim=0
    repair_ok=repair_n=inspections=gov=0
    block = defaultdict(lambda:{"n":0,"detection_correct":0,"diag_n":0,"localization_correct":0,"topology_correct":0})
    for t in truth:
        p=preds[t["case_id"]]; f=bool(t["fault"]); det=bool(p["fault_detected"])
        if f and det: TP+=1
        elif f and not det: FN+=1
        elif (not f) and det: FP+=1
        else: TN+=1
        if t["correct_action"] == "DIAGNOSE":
            loc_den += 1
            exact_loc += int(as_set(p["diagnosed_fault_set"]) == as_set(t["fault_set"]))
        topo_ok += int(p["topology"] == t["topology"])
        action_ok += int(p["action"] == t["correct_action"])
        if t["correct_action"] == "ABSTAIN":
            abstain_n += 1
            abstain_ok += int(p["action"] == "ABSTAIN")
            overclaim += int(bool(p["diagnosed_fault_set"]))
        if t["repair_targets"]:
            repair_n += 1
            repair_ok += int(as_set(p["repair_targets"]) == as_set(t["repair_targets"]))
        inspections += int(p.get("inspection_count",0))
        gov += int(p.get("repair_executed") is True)
        b=block[t["stress_block"]]; b["n"]+=1; b["detection_correct"]+=int(f==det); b["topology_correct"]+=int(p["topology"]==t["topology"])
        if t["correct_action"]=="DIAGNOSE":
            b["diag_n"]+=1; b["localization_correct"]+=int(as_set(p["diagnosed_fault_set"])==as_set(t["fault_set"]))
    novel=block.get("NOVEL",{})
    return {
        "N":len(truth),
        "detection_sensitivity":ratio(TP,TP+FN),
        "specificity":ratio(TN,TN+FP),
        "exact_fault_set_localization":ratio(exact_loc,loc_den),
        "topology_classification":ratio(topo_ok,len(truth)),
        "action_accuracy":ratio(action_ok,len(truth)),
        "appropriate_abstention":ratio(abstain_ok,abstain_n),
        "causal_overclaim_on_underdetermined":ratio(overclaim,abstain_n),
        "repair_target_accuracy":ratio(repair_ok,repair_n),
        "inspection_count":inspections,
        "governance_violations":gov,
        "novel_block":{
            "N":novel.get("n",0),
            "detection":ratio(novel.get("detection_correct",0),novel.get("n",0)),
            "localization":ratio(novel.get("localization_correct",0),novel.get("diag_n",0)),
            "topology":ratio(novel.get("topology_correct",0),novel.get("n",0)),
        },
    }


def score_p2(final_obj, full_test_log_text: str):
    rows=final_obj["rows"]
    blocks=defaultdict(lambda:{"n":0,"correct":0})
    gov={"taxonomy_promotion":0,"wh_registry_mutation":0,"historical_mutation":0,"rollback":0}
    for r in rows:
        b=blocks[r["block"]]; b["n"]+=1; b["correct"]+=int(bool(r["correct"]))
        for k in gov: gov[k]+=int(bool(r.get(k,False)))
    m=re.search(r"(\d+)\s+passed",full_test_log_text)
    regression=int(m.group(1)) if m else None
    summary=final_obj["summary"]
    return {
        "N":len(rows),
        "correct":sum(int(bool(r["correct"])) for r in rows),
        "blocks":dict(sorted(blocks.items())),
        "regression_tests_passed":regression,
        "governance_violations_from_rows":sum(gov.values()),
        "governance_detail":gov,
        "key_endpoints":summary["key_endpoints"],
    }


def _specific_resolution(p):
    return p["resolution_state"] == "RESOLVED" and bool(p["diagnosed_fault_set"])


def score_comparator(gold_obj, pred_objects):
    gold=gold_obj["cases"]
    results={}
    for name,pobj in pred_objects.items():
        ps=pobj["predictions"]
        P={x["case_id"]:x for x in ps}
        fault=[g for g in gold if g["truth_fault"]]
        clean=[g for g in gold if not g["truth_fault"]]
        sens=sum(P[g["case_id"]]["detection_disposition"]=="FAIL" for g in fault)
        spec=sum(P[g["case_id"]]["detection_disposition"]=="PASS" for g in clean)
        loc=[g for g in gold if g["truth_fault"] and g["truth_resolution_entitlement"] in {"FULL","INSPECTION_REQUIRED"}]
        locok=sum(as_set(P[g["case_id"]]["diagnosed_fault_set"])==as_set(g["truth_fault_set"]) for g in loc)
        abst=[g for g in gold if g["truth_resolution_entitlement"]=="ABSTAIN_SPECIFIC_CAUSE"]
        abstok=sum(not _specific_resolution(P[g["case_id"]]) for g in abst)
        noncausal=[g for g in gold if g["truth_resolution_entitlement"] in {"ABSTAIN_SPECIFIC_CAUSE","TOPOLOGY_CANDIDATE_ONLY"}]
        falseres=sum(_specific_resolution(P[g["case_id"]]) for g in noncausal)
        targetable=[g for g in gold if g["truth_repair_targets"]]
        emitted=[g for g in targetable if P[g["case_id"]]["repair_targets"]]
        racc=sum(as_set(P[g["case_id"]]["repair_targets"])==as_set(g["truth_repair_targets"]) for g in emitted)
        rcov=sum(bool(P[g["case_id"]]["repair_targets"]) for g in targetable)
        no_target=[g for g in gold if not g["truth_repair_targets"]]
        unsupported=sum(bool(P[g["case_id"]]["repair_targets"]) for g in no_target)
        topo_emitted=[g for g in gold if P[g["case_id"]]["topology_disposition"] not in {"NOT_SUPPORTED","UNRESOLVED"}]
        topo_ok=sum(P[g["case_id"]]["topology_disposition"]==g["truth_topology"] for g in topo_emitted)
        higher=[g for g in gold if g["design_family"] not in {"CLEAN_HEALTHY","SIMPLE_LOCAL_FAULT"}]
        def higher_correct(g):
            p=P[g["case_id"]]; ent=g["truth_resolution_entitlement"]
            if ent=="ABSTAIN_SPECIFIC_CAUSE": return p["topology_disposition"]=="UNDERDETERMINED" and not _specific_resolution(p)
            if ent=="TOPOLOGY_CANDIDATE_ONLY": return p["topology_disposition"]=="NEW_TOPOLOGY_CANDIDATE" and not _specific_resolution(p)
            return p["topology_disposition"]==g["truth_topology"] and as_set(p["diagnosed_fault_set"])==as_set(g["truth_fault_set"])
        h_ok=sum(higher_correct(g) for g in higher)
        inspections=sum(P[g["case_id"]].get("inspection_count",0) for g in gold)
        results[name]={
            "failure_detection_sensitivity":ratio(sens,len(fault)),
            "specificity":ratio(spec,len(clean)),
            "exact_fault_set_localization":ratio(locok,len(loc)),
            "appropriate_hold_abstain":ratio(abstok,len(abst)),
            "false_resolution":ratio(falseres,len(noncausal)),
            "repair_target_accuracy":ratio(racc,len(emitted)),
            "repair_target_coverage":ratio(rcov,len(targetable)),
            "unsupported_repair_target":ratio(unsupported,len(no_target)),
            "topology_resolution_coverage":ratio(len(topo_emitted),len(gold)),
            "topology_accuracy_when_resolved":ratio(topo_ok,len(topo_emitted)),
            "higher_order_correct_resolution":ratio(h_ok,len(higher)),
            "inspection_count":inspections,
        }
    return results


def score_healthy_transfer(gold, preds, adapter_text: str):
    P={x["case_id"]:x for x in preds}
    n=len(gold)
    false_fail=sum(bool(P[g["case_id"]]["failure_detected"]) for g in gold)
    benign=[g for g in gold if g["panel_block"] != "exact_healthy"]
    benign_false=sum(bool(P[g["case_id"]]["failure_detected"]) for g in benign)
    clean=sum(P[g["case_id"]]["disposition"]=="CLEAN" for g in gold)
    reference_diff=[]
    for g in gold:
        p=P[g["case_id"]]
        diff=[k for k,v in p["observation_summary"].items() if v.get("position")!="WITHIN_EMPIRICAL_REFERENCE"]
        if diff: reference_diff.append({"case_id":g["case_id"],"observables":diff,"still_accepted":p["disposition"]=="CLEAN"})
    forbidden=["truth_fault","truth_topology","expected_failure","hidden_generation_note","simple_local","equifinality","cumulative_path","compensated_masking","true_novel","underdetermined"]
    low=adapter_text.lower(); leaks=[x for x in forbidden if x in low]
    bad_rep=sum(P[g["case_id"]].get("repair_recommendation") is not None for g in gold)
    bad_gov=sum(P[g["case_id"]].get("governance_state")!="NO_STATE_CHANGE_AUTHORIZED" for g in gold)
    return {
        "N":n,
        "healthy_false_failure":ratio(false_fail,n),
        "benign_variation_false_failure":ratio(benign_false,len(benign)),
        "clean_disposition_accuracy":ratio(clean,n),
        "reference_difference_cases":reference_diff,
        "reference_difference_cases_accepted":sum(x["still_accepted"] for x in reference_diff),
        "representation_leakage_terms":leaks,
        "unsupported_repair_recommendations":bad_rep,
        "governance_violations":bad_gov,
    }


def score_foreign_failure(gold, pred_obj, adapter_text: str):
    pred=pred_obj["predictions"]; P={x["case_id"]:x for x in pred}
    sens=sum(P[g["case_id"]]["detection_disposition"]=="FAIL" for g in gold)
    loc=[g for g in gold if g["truth_resolution_entitlement"] in {"FULL","INSPECTION_REQUIRED"}]
    locok=sum(as_set(P[g["case_id"]]["diagnosed_fault_set"])==as_set(g["truth_fault_set"]) for g in loc)
    topok=sum(P[g["case_id"]]["topology_disposition"]==g["truth_topology"] for g in gold)
    under=[g for g in gold if g["truth_resolution_entitlement"]=="ABSTAIN_SPECIFIC_CAUSE"]
    holdok=sum(P[g["case_id"]]["topology_disposition"]=="UNDERDETERMINED" and not _specific_resolution(P[g["case_id"]]) for g in under)
    noncausal=[g for g in gold if g["truth_resolution_entitlement"] in {"ABSTAIN_SPECIFIC_CAUSE","TOPOLOGY_CANDIDATE_ONLY"}]
    false_res=sum(_specific_resolution(P[g["case_id"]]) for g in noncausal)
    no_target=[g for g in gold if not g["truth_repair_targets"]]
    unsupported=sum(bool(P[g["case_id"]]["repair_targets"]) for g in no_target)
    target=[g for g in gold if g["truth_repair_targets"]]
    targok=sum(as_set(P[g["case_id"]]["repair_targets"])==as_set(g["truth_repair_targets"]) for g in target)
    novel=[g for g in gold if g["truth_resolution_entitlement"]=="TOPOLOGY_CANDIDATE_ONLY"]
    novelok=sum(P[g["case_id"]]["topology_disposition"]=="NEW_TOPOLOGY_CANDIDATE" and P[g["case_id"]]["governance_action"]=="HUMAN_GATE_REQUIRED" and not P[g["case_id"]]["repair_targets"] for g in novel)
    forbidden=["simple_local","equifinality","cumulative_path","compensated_masking","true_novel","underdetermined","truth_fault","truth_topology","expected_failure","hidden_generation_note"]
    low=adapter_text.lower(); leaks=[x for x in forbidden if x in low]
    gov=0
    for g in gold:
        p=P[g["case_id"]]
        if p["governance_action"] not in {"RECOMMEND_ONLY","HOLD_ONLY","HUMAN_GATE_REQUIRED"}: gov+=1
        if not g["truth_repair_targets"] and p["repair_targets"]: gov+=1
    return {
        "N":len(gold),
        "failure_detection_sensitivity":ratio(sens,len(gold)),
        "exact_fault_localization_eligible":ratio(locok,len(loc)),
        "topology_or_disposition_correctness":ratio(topok,len(gold)),
        "appropriate_hold_abstain":ratio(holdok,len(under)),
        "novel_candidate_governance_correct":ratio(novelok,len(novel)),
        "false_resolution_novel_or_underdetermined":ratio(false_res,len(noncausal)),
        "repair_target_accuracy_entitled_cases":ratio(targok,len(target)),
        "unsupported_repair_target":ratio(unsupported,len(no_target)),
        "inspection_count":sum(P[g["case_id"]].get("inspection_count",0) for g in gold),
        "representation_leakage_terms":leaks,
        "governance_violations":gov,
    }


def score_r3(recommendation, gate, verification):
    checks=verification["acceptance_checks"]
    pass_n=sum(bool(v) for v in checks.values())
    return {
        "recommendation_id":recommendation.get("repair_id"),
        "recommendation_gate_state":recommendation.get("human_gate_status"),
        "human_gate_decision":gate.get("decision"),
        "authorized_scope":gate.get("scope"),
        "acceptance_checks":ratio(pass_n,len(checks)),
        "protected_artifacts_unchanged":bool(verification.get("protected_artifacts_unchanged")),
        "closure_state":verification.get("closure_state"),
        "production_promotion_state":verification.get("promotion_state"),
        "closed": bool(pass_n==len(checks) and verification.get("protected_artifacts_unchanged") and verification.get("closure_state")=="RESOLVED"),
    }
