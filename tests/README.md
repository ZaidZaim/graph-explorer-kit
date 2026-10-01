# Running tests

Run the service-free tests with `uv run --extra dev pytest` and lint with
`uv run --extra dev ruff check src projects tests`. Model credentials are not needed.

The ingestion integration tests opt in through `GRAPHRAG_TEST_URI`. They exercise
real Cypher and APOC merging, use an explicit test connection rather than the
application's `.env`, require an empty database, and roll back every test.

For example, in PowerShell, using a separate disposable Neo4j container:

```powershell
docker run -d --name graphrag-integrity-tests `
  -p 127.0.0.1:57689:7687 `
  -e NEO4J_AUTH=neo4j/integrity-tests-only `
  -e 'NEO4J_PLUGINS=["apoc"]' `
  neo4j:2026.09.0-community
# Wait until logs report Started before running tests.
docker logs graphrag-integrity-tests
$env:GRAPHRAG_TEST_URI = 'bolt://127.0.0.1:57689'
$env:GRAPHRAG_TEST_PASSWORD = 'integrity-tests-only'
uv run --extra dev pytest
docker rm -f -v graphrag-integrity-tests
```

Optional `GRAPHRAG_TEST_USERNAME` and `GRAPHRAG_TEST_DATABASE` default to `neo4j`.
Use a dedicated instance: these tests deliberately exercise broad owned-graph
resolution inside rollback transactions. The tests cover adopted records,
shared provenance, exact-name identity, custom evidence fields, resolution
scopes, colliding filenames, retry cleanup, and lexical graph naming.
