import json
import os
from collections import defaultdict

input_path = os.path.join("data", "dev.txt")
output_path = os.path.join("data", "med_abstracts.json")

parsed_abstracts = []
current_paper = defaultdict(str)
current_pmid = None

with open(input_path, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        if line.startswith("###"):
            # Save previous paper
            if current_pmid and current_paper:
                parsed_abstracts.append({
                    "pmid": current_pmid,
                    **current_paper
                })
                current_paper = defaultdict(str)

            current_pmid = line[3:]  # Remove ###
        else:
            try:
                section, content = line.split("\t", 1)
                current_paper[section.lower()] += content.strip() + " "
            except ValueError:
                print(f"Skipping malformed line: {line}")

# Add last paper
if current_pmid and current_paper:
    parsed_abstracts.append({
        "pmid": current_pmid,
        **current_paper
    })

# Save to JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(parsed_abstracts, f, indent=2)

print(f"Saved {len(parsed_abstracts)} papers to {output_path}")
