# GitHub automation contract

GitHub gives `.github/README.md` precedence on the repository homepage. Keep it
identical to the root reader README, prefixing each local link/image path with
`../` for this folder. The publication verifier rejects drift between the two.
Automation documentation belongs in `workflows/README.md`.

Read [workflows/AGENTS.md](workflows/AGENTS.md) before editing workflows.
Use read-only permissions and immutable action revisions. Keep event triggers
and validation scope explicit in the workflow documentation. Reproduce
commands locally, then verify the actual hosted run for the changed commit.
Keep publication and credentialed operations outside the Python check workflow.
