import os
import json
import csv
from src.logger import logger

def generate_summary(metrics_dir="reports/metrics", output_file="reports/summary.csv"):
    summary_data = []

    # Collect all JSON metric files
    for file_name in os.listdir(metrics_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(metrics_dir, file_name)
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    summary_data.append({
                        "Model": data.get("model", "unknown"),
                        "Prompt": data.get("prompt", "unknown"),
                        "Function Score": data.get("function_score", 0),
                        "Final Score": data.get("final_score", 0.0)
                    })
            except Exception as e:
                logger.error(f" Failed to process {file_name}: {e}")

    # Save to CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Model", "Prompt", "Function Score", "Final Score"])
        writer.writeheader()
        writer.writerows(summary_data)

    logger.info(f" Summary saved to {output_file}")

if __name__ == "__main__":
    generate_summary()
