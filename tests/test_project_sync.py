from tools.add_pulse_issues_to_project import DEFAULT_ISSUES, parse_args


def test_project_sync_defaults_to_lens_pulse_issues():
    assert DEFAULT_ISSUES == (152, 153, 154, 155, 156, 157, 158)


def test_project_sync_accepts_custom_issue_numbers():
    args = parse_args(["--issue", "1", "--issue", "2", "--project", "7"])

    assert args.issues == [1, 2]
    assert args.project == 7

