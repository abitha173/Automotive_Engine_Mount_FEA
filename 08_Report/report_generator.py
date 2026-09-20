"""Simple report generation hook for the CAE project."""
from pathlib import Path


def build_report(report_path: str):
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('CAE Project Report
===================

Status: draft ready
', encoding='utf-8')
    return str(path)


if __name__ == '__main__':
    print(build_report('08_Report/CAE_Project_Report.txt'))
