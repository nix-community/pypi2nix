import os
import os.path
import zipfile


class WheelBuilder:
    def __init__(
        self, requirements_files, setup_requirements_files, pip, project_directory
    ):
        self.requirements_files = requirements_files
        self.setup_requirements_files = setup_requirements_files
        self.pip = pip
        self.download_directory = os.path.join(project_directory, "download")
        self.wheel_directory = os.path.join(project_directory, "wheel")
        self.extracted_wheels_directory = os.path.join(project_directory, "wheelhouse")
        self.indexes = [self.wheel_directory]

    def build(self):
        self.pip.download_sources(
            requirements=self.setup_requirements_files,
            constraints=self.requirements_files,
            target_directory=self.download_directory,
        )
        self.pip.build_wheels(
            requirements=self.setup_requirements_files,
            target_directory=self.wheel_directory,
            source_directories=[self.download_directory],
        )
        self.pip.install(
            requirements=self.setup_requirements_files, source_directories=self.indexes
        )

        self.pip.download_sources(
            requirements=self.requirements_files,
            target_directory=self.download_directory,
        )
        self.pip.build_wheels(
            requirements=self.requirements_files,
            target_directory=self.wheel_directory,
            source_directories=[self.download_directory],
        )

        self.pip.install(
            requirements=self.requirements_files, source_directories=self.indexes
        )
        return self.extract_wheels()

    def extract_wheels(self):
        try:
            os.makedirs(self.extracted_wheels_directory)
        except FileExistsError:
            pass

        wheels = [
            file_path
            for file_path in list_files(self.wheel_directory)
            if os.path.isfile(file_path) and file_path.endswith(".whl")
        ]
        for wheel in wheels:
            zip_file = zipfile.ZipFile(wheel)
            zip_file.extractall(self.extracted_wheels_directory)
            zip_file.close()

        return [
            dist_info
            for dist_info in list_files(self.extracted_wheels_directory)
            if dist_info.endswith(".dist-info")
        ]


def list_files(path):
    return map(lambda f: os.path.join(path, f), os.listdir(path))
