# Mission 169 - Bundle Inspector
# Summarise the contents of a deployment bundle (zip archive).
import zipfile

ARTIFACT_SUFFIXES = (".whl", ".jar")


def inventory(zip_path):
    artifacts = []
    files = 0
    total = 0
    with zipfile.ZipFile(zip_path) as bundle:
        for info in bundle.infolist():
            files += 1
            total += info.compress_size
            if info.filename.endswith(ARTIFACT_SUFFIXES):
                artifacts.append(info.filename)
    return {"artifacts": sorted(artifacts), "files": files, "total_size": total}
