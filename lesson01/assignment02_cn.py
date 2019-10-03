import random

response_rules = {
    '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y'],
    '?*x喜欢?*y': ['喜欢?y的哪里？', '?y有什么好的呢？', '你想要?y吗？']
}

def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}

def subsitite(rule, parsed_rules):
    if not rule: return []

    return [parsed_rules.get(rule[0], rule[0])] + subsitite(rule[1:], parsed_rules)

def is_variable(pattern):
    return pattern.startswith('?') and all(s.isalpha() for s in pattern[1:2])

def is_pattern_segment(pattern):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:3])

def is_match(rest, saying):
    if not rest and not saying:
        return True
    if not all(a.isalpha() for a in rest[0]):
        return True
    if rest[0] != saying[0]:
        return False
    return is_match(rest[1:], saying[1:])

def pat_split(pattern):
    pattern_list = []
    if is_variable(pattern):
        pattern_list += [pattern[0:2]] + pat_split(pattern[2:])
    elif is_pattern_segment(pattern):
        pattern_list += [pattern[0:3]] + pat_split(pattern[3:])
    else:
        

def to_re_pattern(pattern):
    re_pattern =

def segment_match(pattern, saying):
    seg_pat, rest = pattern[0], pattern[1:]
    seg_pat = seg_pat.replace('?*', '?')

    if not rest: return (seg_pat, saying), len(saying)

    for i, token in enumerate(saying):
        if rest[0] == token and is_match(rest[1:], saying[(i + 1):]):
            return (seg_pat, saying[:i]), i

    return (seg_pat, saying), len(saying)

def pat_match_with_seg(pattern, saying):
    if is_variable(pat):
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif is_pattern_segment(pattern):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return []

def get_response(saying, rules):
    #saying_list = saying.split()
    for pattern, responses in rules.items():
        #pattern_list = to_seg(pattern)
        matched_list = pat_match_with_seg(pattern, saying)
        if len(matched_list):
            matched_dict = pat_to_dict(matched_list)
            response_list = to_seg(random.choice(responses))
            return ''.join(subsitite(response_list, matched_dict))
    return ''

if __name__ == '__main__':
    print(get_response("妈妈我想要苹果手机", response_rules))
