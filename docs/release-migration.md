# Release migration

1. Merge the tools PR and run **Prepare dataset release** under GitHub Actions.
   It reads the original ZIPs from the pinned historical commit, audits them, and
   uploads them to a draft `v1.0.0` release. No rewritten or regenerated images are used.
2. Review all eleven ZIP assets and their SHA-256 checksums. Resolve licensing and
   inspect `data/audit.json` issues before publishing the draft release.
3. Only after the release is published, run `python scripts/remove_released_archives.py`.
   The script checks published release asset names and byte sizes against the audit
   before staging deletion of the repository ZIPs. Commit and review that deletion.
4. Update the README download section to link the published release.

Deleting files does not shrink existing Git history. Purging binary history requires a
separate coordinated migration, verified backups, and an explicit force-push decision.
Do not rewrite shared history as part of this PR. If history is later rewritten,
archive the pinned source snapshot separately first and update the release workflow;
its historical commit must remain reachable until migration completes.
