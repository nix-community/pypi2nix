import os
import os.path
import zipfile


class WheelBuilder:
    def __init__(self, pip, project_directory):
        self.pip = pip
        self.download_directory = os.path.join(project_directory, "download")
        self.wheel_directory = os.path.join(project_directory, "wheel")
        self.extracted_wheels_directory = os.path.join(project_directory, "wheelhouse")
        self.indexes = [self.wheel_directory]

    def build(self, requirements_files, setup_requirements_files):
        self.pip.download_sources(
            requirements=setup_requirements_files,
            constraints=requirements_files,
            target_directory=self.download_directory,
        )
        self.pip.build_wheels(
            requirements=setup_requirements_files,
            target_directory=self.wheel_directory,
            source_directories=[self.download_directory],
        )
        self.pip.install(
            requirements=setup_requirements_files, source_directories=self.indexes
        )

        self.pip.download_sources(
            requirements=requirements_files, target_directory=self.download_directory
        )
        self.pip.build_wheels(
            requirements=requirements_files,
            target_directory=self.wheel_directory,
            source_directories=[self.download_directory],
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
            try:
                zip_file.extractall(self.extracted_wheels_directory)
            finally:
                zip_file.close()

        return [
            dist_info
            for dist_info in list_files(self.extracted_wheels_directory)
            if dist_info.endswith(".dist-info")
        ]

    def get_frozen_requirements(self):
        return self.pip.freeze(python_path=[self.extracted_wheels_directory])


def list_files(path):
    return map(lambda f: os.path.join(path, f), os.listdir(path))
