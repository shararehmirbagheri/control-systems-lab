import csv
from pathlib import Path


def compare_files(file1_path, file2_path, output_csv):
    file1 = Path(file1_path)
    file2 = Path(file2_path)

    lines1 = file1.read_text(encoding="utf-8").splitlines()
    lines2 = file2.read_text(encoding="utf-8").splitlines()

    max_lines = max(len(lines1), len(lines2))

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Line Number",
            f"{file1.name}",
            f"{file2.name}",
            "Status"
        ])

        for i in range(max_lines):
            line1 = lines1[i] if i < len(lines1) else ""
            line2 = lines2[i] if i < len(lines2) else ""

            if line1 != line2:
                writer.writerow([
                    i + 1,
                    line1,
                    line2,
                    "Different"
                ])

    print(f"Comparison complete. Results saved to: {output_csv}")


# Compare these two files
compare_files(
    "power_calculator.py",
    "power_calculator2.py",
    "code_differences.csv"
)