import json
import sys
from japverbconj.constants.enumerated_types import Formality, Polarity, Tense, VerbClass
from japverbconj.verb_form_gen import generate_japanese_verb_by_str

verb = sys.argv[1]
#verb = '読む'
verb_class = VerbClass.GODAN

conjugations = {
  "plain": generate_japanese_verb_by_str(verb, verb_class, "pla"),
  "plain_neg": generate_japanese_verb_by_str(verb, verb_class, "pla", "neg"),
  "polite": generate_japanese_verb_by_str(verb, verb_class, "pol"),
  "polite_neg": generate_japanese_verb_by_str(verb, verb_class, "pol", "neg"),
  "plain_past": generate_japanese_verb_by_str(verb, verb_class, "pla", "past"),
  "plain_past_neg": generate_japanese_verb_by_str(verb, verb_class, "pla", "past", "neg"),
  "polite_past": generate_japanese_verb_by_str(verb, verb_class, "pol", "past"),
  "polite_past_neg": generate_japanese_verb_by_str(verb, verb_class, "pol", "past", "neg"),
  "te_form": generate_japanese_verb_by_str(verb, verb_class, "te"),
  "te_form_neg": generate_japanese_verb_by_str(verb, verb_class, "te", "neg"),
  "potential": generate_japanese_verb_by_str(verb, verb_class, "pot"),
  "potential_neg": generate_japanese_verb_by_str(verb, verb_class, "pot", "neg"),
  "passive": generate_japanese_verb_by_str(verb, verb_class, "pass"),
  "passive_neg": generate_japanese_verb_by_str(verb, verb_class, "pass", "neg"),
  "causative": generate_japanese_verb_by_str(verb, verb_class, "caus"),
  "causative_neg": generate_japanese_verb_by_str(verb, verb_class, "caus", "neg"),
  "imperative": generate_japanese_verb_by_str(verb, verb_class, "imp"),
  "imperative_neg": generate_japanese_verb_by_str(verb, verb_class, "imp", "neg"),
  "volitional": generate_japanese_verb_by_str(verb, verb_class, "vol"),
  "volitional_neg": generate_japanese_verb_by_str(verb, verb_class, "vol", "neg"),
  "provisional": generate_japanese_verb_by_str(verb, verb_class, "prov"),
  "provisional_neg": generate_japanese_verb_by_str(verb, verb_class, "prov", "neg"),
  "conditional": generate_japanese_verb_by_str(verb, verb_class, "cond"),
  "conditional_neg": generate_japanese_verb_by_str(verb, verb_class, "cond", "neg")
}

json_output = json.dumps(conjugations, ensure_ascii=False, indent=4)
print(json_output)
