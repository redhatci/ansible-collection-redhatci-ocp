## Metadata structure

The metadata resides in the event object under `.metadata[]`
When everything is properly done, it has the following sections

```yaml
---
ci: # data about the CI
  # general info - urls, types
  runner: # information about the runner
    # runner details, info about h/w, os

pipeline: # information current pipeline when relevant
  # pipeline details/urls

job:  # information about the job

source:
  # source code info
  change: # information about the change/pr/mr
    # details about the change

product: ## information about the product
```