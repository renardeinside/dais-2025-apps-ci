import shutil
from typing import Any
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from pathlib import Path


class BuildHook(BuildHookInterface):
    """Custom build hook for Databricks Apps.

    This hook is used to:
    1. build the UI assets for the Databricks Apps project
    2. Prepare the wheel for Databricks Apps by copying it to a ./.build folder
    3. Write a requirements.txt file in the ./.build folder with the name of the wheel

    Please note that Ui assets are build before the wheel is built.
    """

    def finalize(
        self, version: str, build_data: dict[str, Any], artifact_path: str
    ) -> None:
        self.app.display_info(
            f"✨ Running Databricks Apps build hook for project {self.metadata.name} in directory {Path.cwd()}"
        )
        # remove the ./.build folder if it exists
        build_dir = Path(".build")
        self.app.display_info(f"📂 Resulting build directory: {build_dir.absolute()}")

        if build_dir.exists():
            self.app.display_info(f"🗑️ Removing {build_dir}")
            shutil.rmtree(build_dir)
            self.app.display_info(f"✅ Removed {build_dir}")

        # copy the artifact_path to the ./.build folder
        build_dir.mkdir(exist_ok=True)
        self.app.display_info(f"📋 Copying {artifact_path} to {build_dir}")
        shutil.copy(artifact_path, build_dir)

        # write the name of the artifact to a requirements.txt file in the ./.build folder

        requirements_file = build_dir / "requirements.txt"
        self.app.display_info(
            f"📝 Writing requirements.txt to {requirements_file.absolute()}"
        )

        requirements_file.write_text(Path(artifact_path).name, encoding="utf-8")

        app_file = Path("app.yml")
        if app_file.exists():
            self.app.display_info(f"📄 Copying {app_file} to {build_dir.absolute()}")
            shutil.copy(app_file, build_dir)

        self.app.display_info(
            f"🎉 Apps-compatible build written to {build_dir.absolute()}"
        )
