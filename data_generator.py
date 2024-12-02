import random
from typing import Dict

def gen_bathroom_features() -> Dict[str, bool]:
    """Generate bathroom features as boolean values."""
    # Base features that are almost always present
    has_toilet = True  # Always present
    has_sink = True    # Always present
    has_shower = random.random() < 0.95
    has_bathtub = random.random() < 0.4
    has_hanging_toilet = random.random() < 0.5
    has_separate_toilet = random.random() < 0.3
    has_double_sink = random.random() < 0.2
    has_shower_enclosure = has_shower and random.random() < 0.5
    has_bubble_function = has_bathtub and random.random() < 0.1
    has_built_in_cabinet = random.random() < 0.6
    has_cabinet_extra_storage = random.random() < 0.4

    return {
        'toilet': has_toilet,
        'hanging_toilet': has_hanging_toilet,
        'separate_toilet': has_separate_toilet,
        'sink': has_sink,
        'double_sink': has_double_sink,
        'shower': has_shower,
        'shower_enclosure': has_shower_enclosure,
        'bathtub': has_bathtub,
        'bubble_function': has_bubble_function,
        'built_in_cabinet': has_built_in_cabinet,
        'cabinet_extra_storage': has_cabinet_extra_storage
    }

def generate_test_observations(n=10):
    observations = []
    for _ in range(n):
        observation = {
            "living_space": random.randint(50, 200),
            "property_type": random.choice(["galerijwoning", "rijwoning hoek", "benedenwoning", "bovenwoning", "rijwoning tussen"]),
            "property_cat": random.choice(["apartment", "house"]),
            **gen_bathroom_features()
        }
        observations.append(observation)
    return observations

if __name__ == "__main__":
    test_data = generate_test_observations(5)
    print("\nGenerated test data sample:")
    for i, data in enumerate(test_data):
        print(f"{i}: {data}")

    print("\nSample bathroom features:")
    bathroom_features = {k: v for k, v in test_data[0].items() if k in [
        'toilet', 'hanging_toilet', 'separate_toilet', 'sink', 'double_sink', 
        'shower', 'shower_enclosure', 'bathtub', 'bubble_function',
        'built_in_cabinet', 'cabinet_extra_storage'
    ]}
    for k, v in bathroom_features.items():
        print(f"{k}: {v} (type: {type(v)})")