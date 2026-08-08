import subprocess
import json

def check_cloud_run_env_var(service_name, region, var_name="GEMINI_API_KEY"):
    """Cek apakah env variable tertentu sudah di-set di Cloud Run service."""
    result = subprocess.run(
        [
            "gcloud", "run", "services", "describe", service_name,
            "--region", region,
            "--format", "json"
        ],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print("Gagal ambil data service:", result.stderr)
        return

    data = json.loads(result.stdout)
    containers = data["spec"]["template"]["spec"]["containers"]
    env_vars = containers[0].get("env", [])

    found = next((e for e in env_vars if e["name"] == var_name), None)

    if found:
        print(f"✅ {var_name} sudah di-set.")
    else:
        print(f"⚠️ {var_name} TIDAK ditemukan di service '{service_name}'.")

    return env_vars


if __name__ == "__main__":
    check_cloud_run_env_var("langflow", "asia-southeast2", "GEMINI_API_KEY")
