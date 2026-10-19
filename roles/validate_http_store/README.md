# validate_http_store

Checks via a round trip that HTTP store is functional.

Writes a short-lived test file into `http_store_dir` with SELinux type
`container_file_t` (the type the httpd container is allowed to read) and
always removes it, even if the HTTP GET fails. Leaving the file behind
caused later `setup_http_store` runs to fail when Podman tried to relabel
the shared data directory.
