import os
import glob
import csv
import json
import argparse
from src.logger import logger


def _collect_report_rows(reports_dir: str, pattern: str = "*_evaluation.json") -> list:
    rows = []
    for file_path in glob.glob(os.path.join(reports_dir, pattern)):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            metrics = data.get("overall_score", {})
            # If metrics is just a number
            overall_score = metrics if isinstance(metrics, (int, float)) else metrics.get("overall_score", 0)

            row = {
                "file": data.get("file"),
                "model": data.get("model"),
                "overall_score": overall_score,
                "compilation_success": data.get("compilation", {}).get("success", False),
                "compilation_errors": data.get("compilation", {}).get("errors_count", 0),
                "compilation_warnings": data.get("compilation", {}).get("warnings_count", 0),
            }
            rows.append(row)
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
    return rows


def _write_csv(rows: list, csv_path: str, sort_by="overall_score", descending=True):
    if not rows:
        logger.warning("No rows to write!")
        return
    rows = sorted(rows, key=lambda r: r.get(sort_by, 0), reverse=descending)
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    logger.info(f"Summary CSV updated: {csv_path}")


def _write_markdown(rows: list, md_path: str, limit: int = 10):
    rows = sorted(rows, key=lambda r: r.get("overall_score", 0), reverse=True)
    with open(md_path, "w") as mdfile:
        mdfile.write("# Evaluation Leaderboard\n\n")
        mdfile.write("| File | Model | Overall Score |\n")
        mdfile.write("|------|-------|---------------|\n")
        for row in rows[:limit]:
            mdfile.write(f"| {row['file']} | {row['model']} | {row['overall_score']} |\n")
    logger.info(f"Summary Markdown updated: {md_path}")


def main():
    parser = argparse.ArgumentParser(description="Rebuild summary CSV and leaderboard")
    parser.add_argument("--reports", default="reports", help="Directory with evaluation JSON reports")
    parser.add_argument("--csv", default="reports/summary.csv", help="Path to output CSV file")
    parser.add_argument("--md", default="reports/leaderboard.md", help="Path to output leaderboard markdown")
    args = parser.parse_args()

    rows = _collect_report_rows(args.reports)
    _write_csv(rows, args.csv)
    _write_markdown(rows, args.md)


if __name__ == "__main__":
    main()
