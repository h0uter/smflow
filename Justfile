publish:
    uv version --bump minor
    uv build
    uv publish