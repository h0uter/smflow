publish:
    uv version --bump minor
    git commit -m "Bump version"
    git tag -a "v$(uv version)" -m "Release v$(uv version)"
    git push origin main --tags
    uv build
    uv publish
