from typing import Optional

class EnvBuilder:
    def __init__(
        self,
        system_site_packages: bool = ...,
        clear: bool = ...,
        symlinks: bool = ...,
        upgrade: bool = ...,
        with_pip: bool = ...,
        prompt: Optional[str] = None,
    ) -> None: ...
    def create(self, env_dir: str) -> None: ...
