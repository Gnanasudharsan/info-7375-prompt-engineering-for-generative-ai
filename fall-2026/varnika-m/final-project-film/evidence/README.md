# Evidence

Everything here is real and was collected on 2026-10-11 by Claude Code (NEU-provisioned) at
Varnika's direction. Nothing here was produced by the planned tool, which does not exist yet.

| File | What it is | How it was made |
|---|---|---|
| `aws-provider-docs/s3_bucket.html.markdown` | The `aws_s3_bucket` resource page from the Terraform AWS provider docs | Downloaded from `hashicorp/terraform-provider-aws` at commit `f4a1d213000a2032755ac7f05bbfd46f8b909255` (main, committed 2026-10-10T01:20:10Z). Byte-identical to the `v6.68.0` release tag (published 2026-10-07). sha256 `5d5653c0d65ad1fa515fa9d96c5b35ae7f29a464d518512bc4794f941067d0d3`. Unmodified. |
| `aws-provider-docs/LICENSE` | The Mozilla Public License 2.0 text that covers that page | Downloaded from the same commit. Kept beside the page because MPL-2.0 requires the licence to travel with copied files. |
| `licence-check.txt` | The licences reported by GitHub for four Terraform-related repositories, plus the release tag | Output of `api.github.com` calls run 2026-10-11T18:45:46Z. |

## The three lines the film uses

From `s3_bucket.html.markdown` (line numbers in this file):

- **Line 54**, top-level argument: `` `bucket` - (Optional, Forces new resource) Name of the bucket. If omitted, Terraform will assign a random, unique name. ``
- **Line 70**, top-level argument: `` `versioning` - (Optional, **Deprecated**) … Use the resource `aws_s3_bucket_versioning` instead. ``
- **Line 221**, inside the replication `destination` block: `` `bucket` - (Required) ARN of the S3 bucket where you want Amazon S3 to store replicas … ``

Lines 54 and 221 are why the project's main risk is real: the same word, `bucket`, is
Optional at the top level and Required inside a nested block on the same page.

## What the licence check does and does not show

It shows the SPDX identifier GitHub reports and the first lines of each LICENSE file. It is not a
legal review. `hashicorp/terraform` (the core tool) is under the Business Source License for
version 1.6.0 and later, so the project will not copy files from it. The AWS provider repository
is MPL-2.0.
