# commit_changes

Automatically stages and commits added, modified, and removed files in a specified directory within a git repository.

## Variables

| Variable         | Default         | Required | Description                                                                                   |
| ---------------- | --------------- | -------- | --------------------------------------------------------------------------------------------- |
| cc_directory     | -               | Yes      | Path to the directory containing changes to commit (must be inside a git repository).         |
| cc_message       | -               | Yes      | Commit message for the git commit.                                                            |
| cc_author_name   | -               | No       | Name of the commit author (overrides global git user.name).                                   |
| cc_author_email  | -               | No       | Email of the commit author (overrides global git user.email).                                 |
| cc_autopush      | false           | No       | Push after the commit if set to true                             .                            |
