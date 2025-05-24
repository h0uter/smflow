publish: update-readme
    uv version --bump patch
    git add pyproject.toml
    git add uv.lock
    git commit -m "Bump version to v$(uv version --short)"
    git tag -a "v$(uv version --short)" -m "Release v$(uv version --short)"
    git push origin main --tags
    uv build
    uv publish
    rm -rf dist

update-readme:
    uvx --from cogapp cog -o README.md -d ./.readme/README.template.md
    git add README.md
