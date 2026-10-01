# Release migration status

Release v1.0.0 is published. All eleven uploaded ZIP assets were verified against
the audited byte counts and GitHub SHA-256 digests before removing repository copies.
GitHub changed spaces to dots in asset names; data/audit.json records this mapping.
Original archive-relative metadata paths and local download filenames remain unchanged.

The Clean dataset Git history workflow runs when its definition is pushed to main,
and can also be started manually. It verifies release assets again, clones all refs,
saves a complete Git bundle as a seven-day Actions artifact, filters Dataset/*.zip
throughout history, and atomically updates branches and tags with explicit leases.
A concurrent update causes the push to fail rather than overwrite new work.
The v1.0.0 tag is rewritten to the equivalent tree without archive files; uploaded
release assets are not modified.

Check the workflow result. If branch/tag protection rejects rewriting, change the
applicable protection for this authorized migration and rerun the workflow.
After successful cleanup, replace old clones with fresh clones. Old pull-request
refs cannot be changed by normal Git pushes; GitHub may retain them or cached objects.
Do not merge old branches back into cleaned history.

The release verification workflow downloads assets from the published release.
It no longer checks out the historical source commit.
