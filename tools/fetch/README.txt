Capture scripts for the quoted legal text (headless Chromium, Docker only; nothing is installed on the host).
Docker must be able to mount the folders (a folder under your home directory works).
  docker run --rm -v $PWD/tools/fetch:/w -v $CAP:/out mcr.microsoft.com/playwright:v1.49.1-noble \
    sh -c "cd /tmp && npm i playwright@1.49.1 >/dev/null 2>&1 && cp /w/dump.mjs . && node dump.mjs '<url>' <name>"
dump.mjs   plain page: writes /out/<name>.txt and .html
expand.mjs page with accordions: writes /out/<name>_expanded.html (the ACLU scenarios are in the page DOM)
az.mjs     ACLU of Arizona accordion page: clicks each item, writes /out/<tag>_<n>.html (args: url tag)
Names used by tools/extract_quotes.py: aclu_en, aclu_es (dump + expand), azen, azes (az.mjs), ars (azleg.gov 13-2412).
