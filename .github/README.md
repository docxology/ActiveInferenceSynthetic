# GitHub automation

[workflows/checks.yml](workflows/checks.yml) runs Python checks on pushes to
`main`, pull requests and manual dispatch. [Workflow documentation](workflows/README.md)
states versions, scope and local reproduction.

The workflow has read-only repository permissions, pinned action revisions and
no publishing credentials. It does not publish a release or Zenodo record.
Read [AGENTS.md](AGENTS.md) before changing automation.
