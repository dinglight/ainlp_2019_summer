import random

response_rules = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"],
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"],
    "?*X hello ?*Y": ["Hi, how do you do?"],
    "I was ?*X": ["Were you really ?X ?", "I already knew you were ?X ."]
}

def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}

def subsitite(rule, parsed_rules):
    if not rule: return []

    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)

def is_variable(pattern):
    return pattern.startswith('?') and all(s.isalpha() for s in pattern[1:])

def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])

def is_match(rest, saying):
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i

    return (seg_pat, saying), len(saying)

def pat_match_with_seg(pattern, saying):
    if not pattern or not saying: return []

    pat = pattern[0]

    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return []


def get_response(saying, rules):
    saying_list = saying.split()
    for pattern, responses in rules.items():
        pattern_list = pattern.split()
        matched_list = pat_match_with_seg(pattern_list, saying_list)
        if len(matched_list):
            matched_dict = pat_to_dict(matched_list)
            response_list = random.choice(responses).split()
            return ' '.join(subsitite(response_list, matched_dict))
    return ''

if __name__ == '__main__':
    print(get_response("I need iPhone", response_rules))
