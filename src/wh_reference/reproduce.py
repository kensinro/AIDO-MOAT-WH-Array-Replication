from __future__ import annotations
from pathlib import Path
import json
from .io import load_json
from .metrics import score_p1, score_p2, score_comparator, score_healthy_transfer, score_foreign_failure, score_r3


def reproduce(data_root: str | Path):
    d=Path(data_root)
    p1=score_p1(load_json(d/'p1/truth_n100.json'), load_json(d/'p1/predictions_n100.json'))
    p2=score_p2(load_json(d/'p2/final_panel_n240.json'), (d/'p2/full_test_log_final.txt').read_text(encoding='utf-8'))
    comp=score_comparator(
        load_json(d/'p3/comparator/gold_n32.json'),
        {k:load_json(d/f'p3/comparator/{k.lower()}_predictions.json') for k in ('FOC','MLC','WH')}
    )
    b1=score_healthy_transfer(
        load_json(d/'p3/healthy_transfer/gold_n8.json'),
        load_json(d/'p3/healthy_transfer/wh_predictions.json'),
        (d/'p3/healthy_transfer/adapter_visible_input.json').read_text(encoding='utf-8')
    )
    b2=score_foreign_failure(
        load_json(d/'p3/foreign_failure/gold_n20.json'),
        load_json(d/'p3/foreign_failure/wh_predictions.json'),
        (d/'p3/foreign_failure/adapter_visible_input.json').read_text(encoding='utf-8')
    )
    r3=score_r3(load_json(d/'r3/recommendation.json'),load_json(d/'r3/human_gate_authorization.json'),load_json(d/'r3/repair_verification.json'))
    return {'package_version':'0.1.0','protocol_1':p1,'protocol_2':p2,'protocol_3_comparator':comp,'protocol_3_healthy_transfer':b1,'protocol_3_foreign_failure':b2,'r3':r3}


def write_report(result, output_dir: str | Path):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    (out/'REPRODUCED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    p1=result['protocol_1']; p2=result['protocol_2']; c=result['protocol_3_comparator']; b1=result['protocol_3_healthy_transfer']; b2=result['protocol_3_foreign_failure']; r3=result['r3']
    lines=[
      '# WH1.0 Reproducibility Report','',
      '## Protocol 1 — boundary stress',
      f"- Detection: {p1['detection_sensitivity']['n']}/{p1['detection_sensitivity']['d']}",
      f"- Specificity: {p1['specificity']['n']}/{p1['specificity']['d']}",
      f"- Exact localization: {p1['exact_fault_set_localization']['n']}/{p1['exact_fault_set_localization']['d']}",
      f"- Topology: {p1['topology_classification']['n']}/{p1['topology_classification']['d']}",
      f"- NOVEL topology: {p1['novel_block']['topology']['n']}/{p1['novel_block']['topology']['d']}",'',
      '## Protocol 2 — open-set governance',
      f"- Final panel: {p2['correct']}/{p2['N']}",
      f"- Regression tests: {p2['regression_tests_passed']}/{p2['regression_tests_passed']}",
      f"- Row-level governance violations: {p2['governance_violations_from_rows']}",'',
      '## Protocol 3 — comparator',
      f"- FOC detection/localization: {c['FOC']['failure_detection_sensitivity']['n']}/{c['FOC']['failure_detection_sensitivity']['d']} ; {c['FOC']['exact_fault_set_localization']['n']}/{c['FOC']['exact_fault_set_localization']['d']}",
      f"- MLC detection/localization: {c['MLC']['failure_detection_sensitivity']['n']}/{c['MLC']['failure_detection_sensitivity']['d']} ; {c['MLC']['exact_fault_set_localization']['n']}/{c['MLC']['exact_fault_set_localization']['d']}",
      f"- WH detection/localization: {c['WH']['failure_detection_sensitivity']['n']}/{c['WH']['failure_detection_sensitivity']['d']} ; {c['WH']['exact_fault_set_localization']['n']}/{c['WH']['exact_fault_set_localization']['d']}",
      f"- WH higher-order resolution: {c['WH']['higher_order_correct_resolution']['n']}/{c['WH']['higher_order_correct_resolution']['d']}",'',
      '## Protocol 3 — foreign transfer',
      f"- Healthy false failure: {b1['healthy_false_failure']['n']}/{b1['healthy_false_failure']['d']}",
      f"- Foreign failure detection: {b2['failure_detection_sensitivity']['n']}/{b2['failure_detection_sensitivity']['d']}",
      f"- Eligible localization: {b2['exact_fault_localization_eligible']['n']}/{b2['exact_fault_localization_eligible']['d']}",
      f"- Topology/disposition: {b2['topology_or_disposition_correctness']['n']}/{b2['topology_or_disposition_correctness']['d']}",'',
      '## R³ closure',
      f"- Acceptance checks: {r3['acceptance_checks']['n']}/{r3['acceptance_checks']['d']}",
      f"- Closure state: {r3['closure_state']}",
      f"- Production promotion: {r3['production_promotion_state']}",'',
      '> This package reproduces frozen result-level qualification metrics. It is not the full WH supervisory engine and does not authorize state-changing action.'
    ]
    (out/'REPRODUCED_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return out
