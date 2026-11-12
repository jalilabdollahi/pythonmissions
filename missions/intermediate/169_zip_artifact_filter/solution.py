# Mission 169 - Bundle Inspector (solution)
# Summarise the contents of a deployment bundle (zip archive).
import zipfile

ARTIFACT_SUFFIXES = (".whl", ".jar")


def inventory(zip_path):
    artifacts = []
    files = 0
    total = 0
    with zipfile.ZipFile(zip_path) as bundle:
        for info in bundle.infolist():
            if info.is_dir():
                continue
            files += 1
            total += info.file_size
            if info.filename.lower().endswith(ARTIFACT_SUFFIXES):
                artifacts.append(info.filename)
    return {"artifacts": sorted(artifacts), "files": files, "total_size": total}
