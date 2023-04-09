import os
import re
import json
from collections import defaultdict


def find_patterns_in_directory(directory):
    pattern_counts = defaultdict(int)
    pattern_examples = defaultdict(str)

    for root, _, files in os.walk(directory):
        for file in files:
            pattern = re.sub(r'\d', '#', file)
            if pattern not in pattern_examples:
                pattern_examples[pattern] = file
            pattern_counts[pattern] += 1

    response = []
    for pattern in pattern_counts:
        response.append(
            (pattern, pattern_counts[pattern], pattern_examples[pattern]))

    response.sort(key=lambda x: x[1], reverse=True)

    return response


if __name__ == '__main__':
    directory = 'E:\\Mi10T'
    unique_patterns = find_patterns_in_directory(directory)

    print("Unique patterns found:")
    # print(unique_patterns)
    list = []
    for pattern, count, example in unique_patterns:
        if count > 5:
            item = {"pattern": pattern,
                    "count": count,
                    "example": example}
            list.append(item)
    # print(f"Pattern: {pattern} - Count: {count} - Example: {example}")
    json_data = json.dumps(list, indent=4)
    print(json_data)
